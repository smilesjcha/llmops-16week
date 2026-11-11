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
  await audience.evaluate(()=>window.courseDeck.show(0));
  await teacher.waitForFunction(()=>document.querySelector('#position').textContent==='1 / 64');
  assert.ok(await teacher.locator('#previous').isDisabled());
  // Every slide sends its own notes, from the final deck DOM.
  for(let i=0;i<64;i++){
   await audience.evaluate(i=>window.courseDeck.show(i),i);
   await teacher.waitForFunction(n=>document.querySelector('#position').textContent===n+' / 64',i+1);
   const expected=await audience.locator('#notes-text section p').first().textContent();
   assert.equal(await teacher.locator('#notes section p').first().textContent(),expected);
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
  const scroll=await teacher.evaluate(()=>scrollY);await teacher.waitForTimeout(1900);
  assert.equal(await teacher.evaluate(()=>scrollY),scroll);assert.equal(await teacher.locator('#jump').inputValue(),'21');
  await teacher.locator('#outline').selectOption('4');
  await audience.waitForFunction(()=>location.hash==='#slide-4');
  await teacher.locator('#flow-next').click();
  await teacher.waitForFunction(()=>document.querySelector('#flow-caption').textContent.startsWith('1/'));
  assert.ok((await audience.locator('.slide.active .walk-caption').textContent()).startsWith('1/'));
  await teacher.reload();await teacher.waitForSelector('body[data-connected=true]');
  assert.equal(await teacher.locator('#position').textContent(),'4 / 64');
  await audience.reload();await teacher.waitForSelector('body[data-connected=true]');
  await teacher.locator('#next').click();await audience.waitForFunction(()=>location.hash==='#slide-5');
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
  for(const width of [1120,768,390]){
   await teacher.setViewportSize({width,height:950});await teacher.evaluate(()=>scrollTo(0,0));await teacher.waitForTimeout(100);
   assert.ok(await teacher.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await teacher.screenshot({path:path.join(out,(target.startsWith('file:')?'file-':'web-')+`teacher-${width}.png`)});
  }
  await teacher.close();assert.equal(await audience.locator('#notes-panel').isVisible(),false);
  const reopened=audience.waitForEvent('popup');await audience.locator('#presenter-button').click();teacher=await reopened;
  await teacher.waitForSelector('body[data-connected=true]');assert.equal(await teacher.locator('#position').textContent(),'53 / 64');
  const closed=teacher.waitForEvent('close');await teacher.locator('#end').click();await closed;
  assert.equal(await audience.locator('html.audience-mode').count(),0);assert.equal(await audience.locator('#notes-panel').isVisible(),false);
  const again=audience.waitForEvent('popup');await audience.locator('#presenter-button').click();teacher=await again;await teacher.waitForSelector('body[data-connected=true]');
  await audience.close();await teacher.waitForSelector('body[data-connected=false]');assert.ok(await teacher.locator('#next').isDisabled());
  results.runs.push({target,slides:64,notes_hidden_on_audience:true,bidirectional:true,flow_steps:true,window_isolation:true,reload_both:true,close_and_reopen:true,fullscreen_sync:true,scroll_preserved:true,mobile_overflow:0});
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
