/** Verify authored walkthroughs, adaptive reading, screenshot zoom and demo links. */
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..'), out=path.join(root,'output/validation/week11');
const url='file://'+path.join(root,'week11/lecture/index.html');
const browser=await chromium.launch({headless:true,channel:'chrome'});
const result={walkthroughs:[],viewports:[],guides:[],errors:[]};
try{
 const page=await browser.newPage({viewport:{width:1500,height:930}});
 page.on('pageerror',e=>result.errors.push(String(e)));
 await page.goto(url);await page.evaluate(()=>document.fonts.ready);
 for(const number of [4,5,21,44]){
  await page.evaluate(n=>window.courseDeck.show(n-1),number);
  const walk=page.locator('.slide.active .diagram-walk');
  const count=await walk.evaluate(e=>JSON.parse(e.dataset.walk).length);
  for(let i=0;i<count;i++){
   await walk.locator('.walk-next').click();
   assert.ok((await walk.locator('.walk-caption').textContent()).startsWith(`${i+1}/`));
   assert.ok(await walk.locator('.walk-active').count()>0);
   const overlap=await walk.evaluate(e=>e.getBoundingClientRect().bottom>e.closest('.slide').querySelector('footer').getBoundingClientRect().top-6);
   assert.equal(overlap,false,'walk overlap '+number);
  }
  await page.emulateMedia({media:'print'});
  assert.equal(await walk.locator('.walk-controls').isVisible(),false);
  assert.ok(await walk.locator('.node').evaluateAll(ns=>ns.every(n=>getComputedStyle(n).opacity==='1')));
  await page.emulateMedia({media:'screen'});
  await walk.locator('.walk-reset').click();
  assert.equal(await walk.locator('.walk-active').count(),0);
  result.walkthroughs.push({page:number,stages:count,print_full_structure:true});
 }
 await page.locator('#chapter-nav button').filter({hasText:'Langfuse 실습'}).click();
 assert.ok(page.url().endsWith('#slide-43'));
 await page.locator('#overview-button').click();
 await page.locator('#overview-search').fill('ZZZ_NO_RESULT');
 assert.ok(await page.locator('#overview-empty').isVisible());
 await page.locator('#overview-search').fill('Langfuse');
 assert.ok(await page.locator('.chapter-items button:visible').count()>0);
 await page.keyboard.press('Escape');
 assert.equal(await page.locator('#overview').isVisible(),false);
 result.chapter_navigation=true;result.overview_search=true;
 await page.emulateMedia({reducedMotion:'reduce'});
 assert.equal(await page.locator('.node').first().evaluate(e=>getComputedStyle(e).transitionDuration),'0s');
 result.reduced_motion=true;
 await page.emulateMedia({reducedMotion:'no-preference'});
 const count=await page.locator('.slide').count();
 for(const [width,height] of [[320,740],[390,844],[768,1024],[1024,768],[1280,800],[1440,600]]){
  await page.setViewportSize({width,height});
  for(let i=0;i<count;i++){
   await page.evaluate(i=>window.courseDeck.show(i),i);
   const extra=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
   assert.ok(extra<=1,`${width} page ${i+1}: overflow ${extra}`);
  }
  await page.evaluate(()=>window.courseDeck.show(51));
  await page.screenshot({path:path.join(out,`conference-${width}-decision.png`),fullPage:true});
  result.viewports.push({width,height,slides:count,document_overflow:0});
 }
 await page.setViewportSize({width:390,height:844});
 await page.evaluate(()=>{window.courseDeck.show(51);window.scrollTo(0,document.documentElement.scrollHeight);});
 await page.locator('#next').click();
 assert.equal(await page.evaluate(()=>window.scrollY),0);result.reading_slide_starts_at_top=true;
 await page.evaluate(()=>window.courseDeck.show(46));
 await page.locator('.slide.active .enlarge').click();await page.locator('#image-zoom').click();
 assert.ok(await page.locator('#image-content').evaluate(e=>e.scrollWidth>e.clientWidth));
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
 await page.keyboard.press('Escape');result.native_image_pan=true;
 await page.setViewportSize({width:1500,height:930});
 for(const file of ['week11/lab/demo/index.html','week11/lab/sample/langfuse/index.html','week11/lab/reports/langfuse/instructor-console.html']){
  await page.goto('file://'+path.join(root,file));
  assert.equal(await page.locator('h1').count(),1);
  const localMissing=[];
  for(const href of await page.locator('a').evaluateAll(as=>as.map(a=>a.getAttribute('href')))){
   if(!href||/^(https?:|#)/.test(href))continue;
   try{await fs.access(path.resolve(path.dirname(path.join(root,file)),href));}catch{localMissing.push(href);}
  }
  assert.deepEqual(localMissing,[],file);
  for(const width of [390,768,1500]){await page.setViewportSize({width,height:930});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1),file);}
  await page.screenshot({path:path.join(out,path.basename(path.dirname(file))+'-guide.png'),fullPage:true});
  result.guides.push({file,local_links_valid:true,mobile_overflow:0});
 }
 assert.deepEqual(result.errors,[]);
 await fs.writeFile(path.join(out,'conference-receipt.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify(result,null,2));
}finally{await browser.close();}
