/** Real Fullscreen API, uncropped 16:9 fitting, exit and unavailable-API recovery. */
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..');
const out=path.join(root,'output/validation/week11-fullscreen');
await fs.mkdir(out,{recursive:true});
const url=process.env.LECTURE_URL||'file://'+path.join(root,'week11/lecture/index.html');
const browser=await chromium.launch({headless:true,channel:'chrome'});
const receipt={url,viewports:[],errors:[]};
try{
 for(const [width,height] of [[1920,1080],[2560,1440],[1440,900],[1280,600],[768,1024]]){
  const page=await browser.newPage({viewport:{width,height},screen:{width,height}});
  page.on('pageerror',e=>receipt.errors.push(String(e)));
  await page.goto(url);await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>window.courseDeck.show(43));
  await page.locator('#fullscreen').click();
  await page.waitForFunction(()=>!!document.fullscreenElement&&document.documentElement.classList.contains('presentation-mode'));
  await page.mouse.move(width/2,height/2);await page.waitForTimeout(2500);
  const layout=await page.locator('.slide.active').evaluate(e=>({rect:e.getBoundingClientRect().toJSON(),width:innerWidth,height:innerHeight,opacity:getComputedStyle(document.querySelector('.controls')).opacity,transform:getComputedStyle(e).transform}));
  const expected=Math.min(layout.width/1440,layout.height/810);
  assert.ok(Math.abs(layout.rect.width-1440*expected)<1);
  assert.ok(Math.abs(layout.rect.height-810*expected)<1);
  assert.ok(Math.abs(layout.rect.x-(layout.width-layout.rect.width)/2)<1);
  assert.ok(Math.abs(layout.rect.y-(layout.height-layout.rect.height)/2)<1);
  assert.equal(layout.opacity,'0');
  assert.ok(await page.locator('.slide.active .architecture').isVisible());
  for(let i=0;i<64;i++){
   await page.evaluate(i=>window.courseDeck.show(i),i);
   const b=await page.locator('.slide.active').boundingBox();
   assert.ok(b.x>=-1&&b.y>=-1&&b.x+b.width<=layout.width+1&&b.y+b.height<=layout.height+1,'cropped slide '+(i+1));
  }
  await page.evaluate(()=>window.courseDeck.show(43));
  await page.screenshot({path:path.join(out,`full-${width}-${height}.png`)});
  await page.emulateMedia({media:'print'});assert.equal(await page.locator('.slide:visible').count(),64);assert.equal(await page.locator('.deck-shell').evaluate(e=>getComputedStyle(e).position),'static');await page.emulateMedia({media:'screen'});
  await page.keyboard.press('ArrowRight');assert.ok(page.url().endsWith('#slide-45'));
  await page.keyboard.press('o');assert.ok(await page.locator('#overview').isVisible());await page.keyboard.press('Escape');
  await page.mouse.move(5,layout.height-4);
  await page.waitForFunction(()=>getComputedStyle(document.querySelector('.controls')).opacity==='1');
  await page.locator('#fullscreen').click();
  await page.waitForFunction(()=>!document.fullscreenElement&&!document.documentElement.classList.contains('presentation-mode'));
  assert.ok(page.url().endsWith('#slide-45'));
  // P works without leaving focus trapped on the just-used button.
  await page.keyboard.press('p');await page.waitForFunction(()=>!!document.fullscreenElement);
  await page.keyboard.press('p');await page.waitForFunction(()=>!document.fullscreenElement);
  receipt.viewports.push({requested:{width,height},actual:{width:layout.width,height:layout.height},scale:expected,slides:64,centered:true,controls_auto_hide:true,api_enter_exit:true,keyboard:true});
  await page.close();
 }
 const denied=await browser.newPage({viewport:{width:1280,height:800}});
 await denied.addInitScript(()=>{Element.prototype.requestFullscreen=()=>Promise.reject(new DOMException('Blocked','NotAllowedError'));});
 await denied.goto(url);await denied.locator('#fullscreen').click();
 await denied.waitForFunction(()=>document.documentElement.classList.contains('presentation-mode'));
 assert.ok((await denied.locator('#presentation-notice').textContent()).includes('제한'));
 await denied.keyboard.press('Escape');
 assert.equal(await denied.locator('html.presentation-mode').count(),0);
 await denied.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'p',ctrlKey:true,bubbles:true})));assert.equal(await denied.locator('html.presentation-mode').count(),0);
 receipt.unavailable_api_fallback=true;receipt.print_shortcut_preserved=true;
 assert.deepEqual(receipt.errors,[]);
 await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2));
 console.log(JSON.stringify(receipt,null,2));
}finally{await browser.close();}
