/** Multi-window sync and lifecycle checks, including isolation and note visibility. */
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import http from 'node:http';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'output/validation/week11-presenter');
await fs.mkdir(out,{recursive:true});
const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.woff2':'font/woff2'};
const server=http.createServer(async(req,res)=>{
 try{let file=path.join(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep))throw Error();if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(await fs.readFile(file));}catch{res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const local=`http://127.0.0.1:${server.address().port}/`,base=process.env.COURSE_BASE_URL||local;
const browser=await chromium.launch({headless:true,channel:'chrome'});
const results={base,runs:[],errors:[]};
async function previews(page,number){
 await page.waitForFunction(n=>document.querySelector('#current-stage').dataset.page===String(n)&&document.querySelector('#current-stage').getAttribute('aria-busy')==='false',number);
 assert.equal(await page.frameLocator('#current-preview').locator('#preview-root').getAttribute('data-page'),String(number));
 assert.equal(await page.frameLocator('#current-preview').locator('.presenter-note').count(),0);
 if(number<64){
  await page.waitForFunction(n=>document.querySelector('#next-stage').dataset.page===String(n+1)&&document.querySelector('#next-stage').getAttribute('aria-busy')==='false',number);
  assert.equal(await page.frameLocator('#next-preview').locator('#preview-root').getAttribute('data-page'),String(number+1));
 }else{assert.ok(await page.locator('#preview-end').isVisible());assert.ok(await page.locator('#expand-next').isDisabled());}
}

async function checkDivider(teacher,audience,target){
 const divider=teacher.locator('#pane-divider'),key='llmops.week11.presenter.previewShare';
 const share=async()=>Number(await divider.getAttribute('aria-valuenow'));
 const progress=()=>teacher.locator('#notes').evaluate(e=>e.scrollTop/(e.scrollHeight-e.clientHeight));
 const dragTo=async percent=>{
  const box=await divider.boundingBox(),bounds=await teacher.locator('.layout').boundingBox();
  await teacher.mouse.move(box.x+box.width/2,box.y+80);await teacher.mouse.down();
  await teacher.mouse.move(bounds.x+(bounds.width-box.width)*percent/100+box.width/2,box.y+80,{steps:12});await teacher.mouse.up();
 };
 await teacher.setViewportSize({width:1440,height:950});await teacher.evaluate(()=>scrollTo(0,0));
 await teacher.locator('#split-reset').click();
 await teacher.locator('#notes').evaluate(e=>e.scrollTop=(e.scrollHeight-e.clientHeight)*.35);
 const revision=await teacher.frameLocator('#current-preview').locator('#preview-root').getAttribute('data-revision');
 await dragTo(35);assert.ok(Math.abs(await share()-35)<.2);assert.ok(Math.abs(await progress()-.35)<.01);
 const small=await teacher.locator('#current-stage').boundingBox();
 await teacher.screenshot({path:path.join(out,(target.startsWith('file:')?'file-':'web-')+'wide-notes.png')});
 await dragTo(65);assert.ok(Math.abs(await share()-65)<.2);assert.ok(Math.abs(await progress()-.35)<.01);
 const large=await teacher.locator('#current-stage').boundingBox();assert.ok(large.width>small.width*1.7,'preview grows with its pane');
 await teacher.waitForFunction(()=>Math.abs(Number(document.querySelector('#current-stage').style.getPropertyValue('--preview-scale'))-document.querySelector('#current-stage').clientWidth/1440)<.002);
 await teacher.screenshot({path:path.join(out,(target.startsWith('file:')?'file-':'web-')+'wide-preview.png')});
 assert.equal(await teacher.frameLocator('#current-preview').locator('#preview-root').getAttribute('data-revision'),revision,'drag does not reload previews');
 assert.equal(await teacher.locator('body.resizing-panes').count(),0);
 // Pointer capture keeps dragging outside the handle; pane minimums prevent clipping.
 for(const pct of [0,100]){
  await dragTo(pct);
  assert.equal(await share(),Number(await divider.getAttribute(pct===0?'aria-valuemin':'aria-valuemax')));
  assert.ok((await teacher.locator('#visual-pane').boundingBox()).width>=280);
  assert.ok((await teacher.locator('#notes-pane').boundingBox()).width>=340);
  assert.ok(await teacher.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 }
 await divider.press('Enter');assert.equal(await share(),47.5);
 await divider.press('ArrowLeft');assert.equal(await share(),45.5);
 await divider.press('Shift+ArrowRight');assert.equal(await share(),55.5);
 await divider.press('Home');assert.equal(await share(),Number(await divider.getAttribute('aria-valuemin')));
 await divider.press('End');assert.equal(await share(),Number(await divider.getAttribute('aria-valuemax')));
 await divider.dblclick();assert.equal(await share(),47.5);
 assert.equal(await audience.locator('#status').textContent(),'53 / 64','resizing must not advance slides');
 assert.equal(await teacher.locator('#font-value').textContent(),'22px');
 await dragTo(65);const saved=await teacher.evaluate(k=>localStorage.getItem(k),key);
 await teacher.reload();await teacher.waitForSelector('body[data-connected=true]');await previews(teacher,53);
 assert.equal(await share(),Number(saved));
 await teacher.locator('#visual-pane').evaluate(e=>e.scrollTop=e.scrollHeight);
 assert.ok(await teacher.locator('#visual-pane').evaluate(e=>e.scrollTop>0));
 await teacher.locator('#next').click();await previews(teacher,54);
 assert.equal(await teacher.locator('#visual-pane').evaluate(e=>e.scrollTop),0,'new slide starts at its current preview');
 await teacher.locator('#previous').click();await previews(teacher,53);
 await teacher.setViewportSize({width:800,height:950});
 await teacher.waitForFunction(()=>Number(document.querySelector('#pane-divider').getAttribute('aria-valuenow'))<60);
 assert.ok((await teacher.locator('#notes-pane').boundingBox()).width>=340);
 assert.equal(await teacher.evaluate(k=>localStorage.getItem(k),key),saved,'window resize must not overwrite preferred ratio');
 await teacher.setViewportSize({width:390,height:950});assert.equal(await divider.isVisible(),false);
 assert.equal(await teacher.locator('#split-reset').isVisible(),false);
 assert.ok(await teacher.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await teacher.setViewportSize({width:1440,height:950});
 await teacher.waitForFunction(n=>Number(document.querySelector('#pane-divider').getAttribute('aria-valuenow'))===n,Number(saved));
 // Aborted pointer gestures must not leave the whole page in drag mode.
 const box=await divider.boundingBox();await teacher.mouse.move(box.x+16,box.y+80);await teacher.mouse.down();
 await divider.dispatchEvent('pointercancel',{pointerId:1});await teacher.mouse.up();
 assert.equal(await teacher.locator('body.resizing-panes').count(),0);
 await teacher.locator('#split-reset').click();assert.equal(await share(),47.5);
}

try{
 for(const target of process.env.COURSE_BASE_URL?[base]:[base,'file://'+root+'/']){
  const ctx=await browser.newContext({viewport:{width:1440,height:1000}});
  ctx.on('page',p=>p.on('pageerror',e=>results.errors.push(String(e))));
  const audience=await ctx.newPage();await audience.goto(target+'week11/lecture/index.html#slide-46');
  const unrelated=await ctx.newPage();await unrelated.goto(target+'week11/lecture/index.html');
  await audience.keyboard.press('n');assert.ok(await audience.locator('#notes-panel').isVisible());
  const popupEvent=audience.waitForEvent('popup');await audience.locator('#presenter-button').click();let teacher=await popupEvent;
  await teacher.waitForSelector('body[data-connected=true]');
  assert.equal(await teacher.locator('#position').textContent(),'46 / 64');
  assert.equal(await audience.locator('#notes-panel').isVisible(),false);assert.equal(await audience.locator('#notes-button').isVisible(),false);
  assert.equal(await teacher.locator('#notes section').count(),7);
  await previews(teacher,46);
  await audience.evaluate(()=>window.courseDeck.show(0));
  await teacher.waitForFunction(()=>document.querySelector('#position').textContent==='1 / 64');
  assert.ok(await teacher.locator('#previous').isDisabled());
  // Every slide sends its own notes, from the final deck DOM.
  for(let i=0;i<64;i++){
   await audience.evaluate(i=>window.courseDeck.show(i),i);
   await teacher.waitForFunction(n=>document.querySelector('#position').textContent===n+' / 64',i+1);
   const expected=await audience.locator('#notes-text section p').first().textContent();
   assert.equal(await teacher.locator('#notes section p').first().textContent(),expected);
   await previews(teacher,i+1);
   assert.equal(await teacher.frameLocator('#current-preview').locator('img').evaluateAll(es=>es.filter(e=>!e.complete||!e.naturalWidth).length),0);
  }
  assert.ok(await teacher.locator('#next').isDisabled());
  assert.equal(await unrelated.locator('#status').textContent(),'1 / 64');
  const secondPopup=unrelated.waitForEvent('popup');await unrelated.locator('#presenter-button').click();const secondTeacher=await secondPopup;
  await secondTeacher.waitForSelector('body[data-connected=true]');await secondTeacher.locator('#next').click();
  await unrelated.waitForFunction(()=>location.hash==='#slide-2');assert.equal(await audience.locator('#status').textContent(),'64 / 64');
  const secondClosed=secondTeacher.waitForEvent('close');await secondTeacher.locator('#end').click();await secondClosed;
  // A duplicated history entry must not reuse the original window's active pair.
  const duplicated=await ctx.newPage();await duplicated.addInitScript(saved=>history.replaceState(saved,'',location.href),await audience.evaluate(()=>history.state));
  await duplicated.goto(target+'week11/lecture/index.html');assert.notEqual(await duplicated.evaluate(()=>history.state.week11Session),await audience.evaluate(()=>history.state.week11Session));
  assert.equal(await duplicated.locator('html.audience-mode').count(),0);await duplicated.close();
  // Only the paired window may control this audience, even with the correct token.
  const session=await audience.evaluate(()=>history.state.week11Session);
  await audience.evaluate(({protocol,session})=>window.postMessage({protocol,session,type:'command',action:'goto',page:2},'*'),{protocol:'llmops-week11-presenter-v1',session});
  await audience.waitForTimeout(100);assert.equal(await audience.locator('#status').textContent(),'64 / 64');
  await teacher.locator('#jump').fill('53');await teacher.locator('#jump-form button').click();
  await audience.waitForFunction(()=>document.querySelector('#status').textContent==='53 / 64');
  await teacher.waitForFunction(()=>document.querySelector('#position').textContent==='53 / 64');
  await teacher.setViewportSize({width:1100,height:900});
  await teacher.evaluate(()=>{window.scrollTo(0,500);document.querySelector('#jump').value='21';});
  await previews(teacher,53);
  // Let the queued responsive fit settle before checking heartbeat scroll preservation.
  await teacher.waitForTimeout(200);
  await teacher.locator('#notes').evaluate(e=>e.scrollTop=200);
  const noteScroll=await teacher.locator('#notes').evaluate(e=>e.scrollTop);
  const revision=await teacher.frameLocator('#current-preview').locator('#preview-root').getAttribute('data-revision');
  const scroll=await teacher.evaluate(()=>scrollY);await teacher.waitForTimeout(1900);
  assert.equal(await teacher.evaluate(()=>scrollY),scroll);assert.equal(await teacher.locator('#jump').inputValue(),'21');
  assert.equal(await teacher.locator('#notes').evaluate(e=>e.scrollTop),noteScroll);
  assert.equal(await teacher.frameLocator('#current-preview').locator('#preview-root').getAttribute('data-revision'),revision);
  await teacher.locator('#font-larger').click();assert.equal(await teacher.locator('#font-value').textContent(),'24px');
  assert.equal(await teacher.locator('#notes').evaluate(e=>getComputedStyle(e).fontSize),'24px');
  const setSize=async value=>teacher.locator('#font-size').evaluate((e,value)=>{e.value=String(value);e.dispatchEvent(new Event('input',{bubbles:true}));},value);
  await setSize(36);assert.ok(await teacher.locator('#font-larger').isDisabled());
  assert.equal(await teacher.frameLocator('#current-preview').locator('body').evaluate(e=>getComputedStyle(e).fontSize),'24px');
  await setSize(16);assert.ok(await teacher.locator('#font-smaller').isDisabled());
  await teacher.locator('#font-reset').click();assert.equal(await teacher.locator('#font-value').textContent(),'22px');
  await setSize(30);await teacher.reload();await teacher.waitForSelector('body[data-connected=true]');await previews(teacher,53);
  assert.equal(await teacher.locator('#font-value').textContent(),'30px');
  await teacher.locator('#expand-current').click();await teacher.waitForFunction(()=>document.querySelector('#expanded-stage').dataset.page==='53');
  assert.ok(await teacher.locator('#preview-dialog').isVisible());await teacher.keyboard.press('Escape');
  await teacher.locator('#expand-next').click();await teacher.waitForFunction(()=>document.querySelector('#expanded-stage').dataset.page==='54');
  await teacher.locator('#preview-close').click();await teacher.locator('#font-reset').click();
  await checkDivider(teacher,audience,target);
  await teacher.locator('#outline').selectOption('4');
  await audience.waitForFunction(()=>location.hash==='#slide-4');
  await teacher.locator('#flow-next').click();
  await teacher.waitForFunction(()=>document.querySelector('#flow-caption').textContent.startsWith('1/'));
  assert.ok((await audience.locator('.slide.active .walk-caption').textContent()).startsWith('1/'));
  await teacher.frameLocator('#current-preview').locator('.walk-caption').filter({hasText:'1/'}).waitFor();
  assert.ok(await teacher.frameLocator('#current-preview').locator('.walk-active').count()>0);
  await teacher.reload();await teacher.waitForSelector('body[data-connected=true]');
  assert.equal(await teacher.locator('#position').textContent(),'4 / 64');
  await audience.reload();await teacher.waitForSelector('body[data-connected=true]');
  await teacher.locator('#next').click();await audience.waitForFunction(()=>location.hash==='#slide-5');
  await audience.evaluate(()=>window.courseDeck.show(15));await previews(teacher,16);
  await audience.locator('#metric-k').evaluate(e=>{e.value='2';e.dispatchEvent(new Event('input',{bubbles:true}));});
  await teacher.frameLocator('#current-preview').locator('#metric-k-label').filter({hasText:'2'}).waitFor();
  await audience.evaluate(()=>location.hash='slide-28');await teacher.waitForFunction(()=>document.querySelector('#position').textContent==='28 / 64');
  await audience.reload();await teacher.waitForSelector('body[data-connected=true]');
  const windows=ctx.pages().length;await audience.locator('#presenter-button').click();await audience.waitForTimeout(100);assert.equal(ctx.pages().length,windows);
  await audience.evaluate(()=>document.activeElement.blur());await audience.keyboard.press('n');assert.equal(await audience.locator('#notes-panel').isVisible(),false);
  await audience.bringToFront();await audience.keyboard.press('p');
  await audience.waitForFunction(()=>!!document.fullscreenElement&&document.documentElement.classList.contains('presentation-mode'));
  await teacher.locator('#next').click();await audience.waitForFunction(()=>location.hash==='#slide-29');
  assert.ok(await audience.evaluate(()=>!!document.fullscreenElement));assert.equal(await audience.locator('#notes-panel').isVisible(),false);
  await audience.waitForFunction(()=>getComputedStyle(document.querySelector('.controls')).opacity==='0');
  await audience.screenshot({path:path.join(out,(target.startsWith('file:')?'file-':'web-')+'audience.png')});
  await audience.keyboard.press('p');await audience.waitForFunction(()=>!document.fullscreenElement);
  await teacher.locator('#outline').selectOption('53');await teacher.waitForFunction(()=>document.querySelector('#position').textContent==='53 / 64');
  await previews(teacher,53);
  for(const width of [1440,1120,768,390]){
   await teacher.setViewportSize({width,height:950});await teacher.evaluate(()=>scrollTo(0,0));await teacher.waitForTimeout(100);
   assert.ok(await teacher.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   if(width>=1120){
    const bounds=await teacher.evaluate(()=>({preview:document.querySelector('#visual-pane').getBoundingClientRect().bottom,notes:document.querySelector('#notes').getBoundingClientRect().bottom,footer:document.querySelector('footer.controls').getBoundingClientRect().top}));
    assert.ok(bounds.preview<=bounds.footer,JSON.stringify(bounds));assert.ok(bounds.notes<=bounds.footer,JSON.stringify(bounds));
    await teacher.locator('#next-stage').scrollIntoViewIfNeeded();
    assert.ok(await teacher.locator('#next-stage').evaluate(e=>{const a=e.getBoundingClientRect(),b=document.querySelector('#visual-pane').getBoundingClientRect();return a.top>=b.top-1&&a.bottom<=b.bottom+1;}));
   }
   await teacher.screenshot({path:path.join(out,(target.startsWith('file:')?'file-':'web-')+`teacher-${width}.png`)});
  }
  await teacher.setViewportSize({width:1440,height:950});await teacher.locator('#pane-divider').press('Shift+ArrowLeft');
  const savedShare=await teacher.locator('#pane-divider').getAttribute('aria-valuenow');
  await teacher.locator('#font-larger').click();
  await teacher.close();assert.equal(await audience.locator('#notes-panel').isVisible(),false);
  const reopened=audience.waitForEvent('popup');await audience.locator('#presenter-button').click();teacher=await reopened;
  await teacher.waitForSelector('body[data-connected=true]');assert.equal(await teacher.locator('#position').textContent(),'53 / 64');
  assert.equal(await teacher.locator('#font-value').textContent(),'24px');
  await teacher.setViewportSize({width:1440,height:950});
  await teacher.waitForFunction(n=>document.querySelector('#pane-divider').getAttribute('aria-valuenow')===n,savedShare);
  const closed=teacher.waitForEvent('close');await teacher.locator('#end').click();await closed;
  assert.equal(await audience.locator('html.audience-mode').count(),0);assert.equal(await audience.locator('#notes-panel').isVisible(),false);
  const again=audience.waitForEvent('popup');await audience.locator('#presenter-button').click();teacher=await again;await teacher.waitForSelector('body[data-connected=true]');
  await audience.close();await teacher.waitForSelector('body[data-connected=false]');assert.ok(await teacher.locator('#next').isDisabled());
  results.runs.push({target,slides:64,notes_hidden_on_audience:true,bidirectional:true,flow_steps:true,window_isolation:true,reload_both:true,close_and_reopen:true,fullscreen_sync:true,scroll_preserved:true,previews:64,live_diagram:true,live_metric:true,preview_zoom:true,font_adjustment_and_persistence:true,divider_drag_keyboard_limits:true,divider_persistence_and_responsive_restore:true,mobile_overflow:0});
  await ctx.close();
 }
 const blocked=await browser.newPage();await blocked.addInitScript(()=>window.open=()=>null);
 await blocked.goto(base+'week11/lecture/index.html');await blocked.locator('#presenter-button').click();
 assert.ok((await blocked.locator('#presenter-feedback').textContent()).includes('팝업이 차단'));
 assert.equal(await blocked.locator('#notes-panel').isVisible(),false);assert.equal(await blocked.locator('#notes-button').isVisible(),false);
 await blocked.locator('#presenter-stop').click();assert.equal(await blocked.locator('html.audience-mode').count(),0);
 const direct=await browser.newPage();await direct.goto(base+'week11/lecture/presenter.html');assert.ok(await direct.locator('#waiting').isVisible());assert.ok(await direct.locator('#next').isDisabled());
 results.popup_blocked_safe=true;results.direct_open_guidance=true;assert.deepEqual(results.errors,[]);
 await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
