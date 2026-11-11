/** Lecturer notes: coverage, navigation, searching, mobile reading and print state. */
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'output/validation/week11-teaching');
await fs.mkdir(out,{recursive:true});
const base=process.env.COURSE_BASE_URL||'file://'+root+'/';
const notes=JSON.parse(await fs.readFile(path.join(root,'week11/lecture/teaching-notes.json')));
const cells=JSON.parse(await fs.readFile(path.join(root,'week11/lab/instructor-notes.json')));
const browser=await chromium.launch({headless:true,channel:'chrome'});
const receipt={base,pages:notes.length,code_cells:cells.length,errors:[],viewports:[]};
try {
 const page=await browser.newPage({viewport:{width:1500,height:930}});
 page.on('pageerror',e=>receipt.errors.push(String(e)));
 await page.goto(base+'week11/lecture/index.html');
 await page.evaluate(()=>document.fonts.ready);
 await page.keyboard.press('n');
 assert.equal(await page.locator('#notes-button').getAttribute('aria-expanded'),'true');
 assert.equal(await page.locator('#notes-panel').evaluate(e=>e.inert),false);
 for(const n of notes){
  await page.evaluate(i=>window.courseDeck.show(i),n.page-1);
  assert.equal(await page.locator('#notes-text section').count(),7);
  assert.ok((await page.locator('#notes-title').textContent()).includes(n.title));
  assert.equal(await page.locator('#notes-text section p').first().textContent(),n.message);
  assert.ok((await page.locator('#instructor-link').getAttribute('href')).endsWith('#page-'+n.page));
 }
 await page.evaluate(()=>{window.courseDeck.show(52);document.querySelector('#notes-panel').scrollTop=1000;});
 await page.keyboard.press('ArrowLeft');
 assert.equal(await page.locator('#notes-panel').evaluate(e=>e.scrollTop),0);
 for(const [width,height] of [[1500,930],[768,1024],[390,844],[320,640]]){
  await page.setViewportSize({width,height});
  const box=await page.locator('#notes-panel').boundingBox();
  assert.ok(box.x>=0&&box.y>=0&&box.x+box.width<=width+1&&box.y+box.height<=height+1);
  assert.ok(await page.locator('#notes-panel').evaluate(e=>e.scrollWidth<=e.clientWidth+1));
 }
 await page.setViewportSize({width:1500,height:930});
 await page.screenshot({path:path.join(out,'presenter-notes.png')});
 await page.locator('#notes-close').click();
 assert.equal(await page.locator('#notes-panel').isVisible(),false);
 assert.equal(await page.locator('#notes-panel').evaluate(e=>e.inert),true);
 await page.keyboard.press('p');await page.waitForFunction(()=>!!document.fullscreenElement&&document.documentElement.classList.contains('presentation-mode'));
 await page.keyboard.press('n');assert.ok(await page.locator('#notes-panel').isVisible());
 await page.emulateMedia({media:'print'});assert.equal(await page.locator('#notes-panel').isVisible(),false);assert.equal(await page.locator('.slide:visible').count(),64);await page.emulateMedia({media:'screen'});
 await page.keyboard.press('p');await page.waitForFunction(()=>!document.fullscreenElement);
 receipt.notes_fullscreen_and_print=true;
 await page.goto(base+'week11/lecture/instructor/index.html');await page.evaluate(()=>document.fonts.ready);
 assert.equal(await page.locator('.summary-table tbody tr').count(),64);
 assert.equal(await page.locator('.page-note').count(),64);assert.equal(await page.locator('.cell-note').count(),18);
 for(const c of cells){
  const node=page.locator(`#cell-${c.notebook}-${c.cell}`);
  assert.ok((await node.textContent()).includes(c.talk));
 }
 const anchorErrors=await page.locator('a[href^="#"]').evaluateAll(as=>as.map(a=>a.hash.slice(1)).filter(id=>!document.getElementById(id)));
 assert.deepEqual(anchorErrors,[]);
 await page.locator('#search').fill('ZZZ_NO_MATCH');assert.equal(await page.locator('.page-note:visible').count(),0);
 await page.locator('#search').fill('HOLD');assert.ok(await page.locator('.page-note:visible').count()>0);
 await page.locator('#expand').click();assert.equal(await page.locator('.page-note:visible:not([open])').count(),0);
 await page.locator('#collapse').click();assert.equal(await page.locator('details[open]').count(),0);
 await page.locator('#priority').selectOption('복습');
 await page.evaluate(()=>location.hash='page-6');
 await page.waitForFunction(()=>document.querySelector('#page-6').open);
 assert.equal(await page.locator('#search').inputValue(),'');assert.equal(await page.locator('#priority').inputValue(),'');
 for(const [width,height] of [[1500,930],[768,1024],[390,844],[320,740]]){
  await page.setViewportSize({width,height});
  for(const id of ['overview','page-53','cell-09-5','cell-10-7']){
   await page.evaluate(id=>location.hash=id,id);
   await page.waitForTimeout(100);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),width+' '+id);
  }
  await page.screenshot({path:path.join(out,`handbook-${width}.png`)});
  receipt.viewports.push({width,height,document_overflow:0});
 }
 await page.setViewportSize({width:1500,height:930});
 await page.evaluate(()=>location.hash='page-53');await page.waitForTimeout(100);
 await page.screenshot({path:path.join(out,'page-53-desktop.png')});
 await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));
 assert.equal(await page.locator('details[open]').count(),82);
 await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});
 await nojs.goto(base+'week11/lecture/instructor/index.html');
 await nojs.locator('#cell-09-5 summary').click();assert.ok(await nojs.locator('#cell-09-5 .detail-body').isVisible());
 assert.ok(await nojs.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 assert.deepEqual(receipt.errors,[]);
 receipt.anchors=true;receipt.filter_and_hash=true;receipt.nojs_readable=true;receipt.print_expands_all=true;
 await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt,null,2));
} finally {await browser.close();}
