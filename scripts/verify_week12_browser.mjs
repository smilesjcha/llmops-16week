import {chromium} from 'playwright';
import path from 'node:path';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'output/validation/week12');
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,channel:'chrome'}),issues=[],errors=[],report={};
try{
 const page=await browser.newPage({viewport:{width:1500,height:930},deviceScaleFactor:1});
 page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('file://'+path.join(root,'week12/lecture/index.html'));await page.evaluate(()=>document.fonts.ready);
 assert.equal(await page.locator('.slide').count(),64);
 for(let i=0;i<64;i++){
  await page.evaluate(i=>window.courseDeck.show(i),i);
  const problem=await page.locator('.slide.active').evaluate(slide=>{
   const rect=slide.getBoundingClientRect(),footer=slide.querySelector('footer').getBoundingClientRect(),result=[];
   for(const el of slide.querySelectorAll('h1,h2,h3,p,pre,table,figure,.row,.flow,.roadmap,svg.architecture,svg.chart')){
    const b=el.getBoundingClientRect();if(b.width===0||el.closest('footer'))continue;
    if(b.left<rect.left-1||b.right>rect.right+1||b.top<rect.top-1||b.bottom>footer.top-6)result.push({tag:el.tagName,text:el.textContent.slice(0,45),bottom:Math.round(b.bottom),footer:Math.round(footer.top)});
    if(el.scrollWidth>el.clientWidth+2)result.push({tag:el.tagName,text:el.textContent.slice(0,40),overflow:el.scrollWidth-el.clientWidth});
   }
   return result;
  });
  if(problem.length)issues.push({page:i+1,issues:problem});
  await page.locator('.slide.active').screenshot({path:path.join(out,'slide-'+String(i+1).padStart(2,'0')+'.png')});
 }
 await page.evaluate(()=>window.courseDeck.show(0));await page.keyboard.press('ArrowRight');assert.ok(page.url().endsWith('#slide-2'));
 await page.locator('#overview-button').click();await page.locator('[data-slide="39"]').click();
 await page.locator('#sample-n').fill('100');await page.locator('#sample-n').dispatchEvent('input');assert.ok((await page.locator('#sample-result').textContent()).includes('[-4.5, 22.1]'));
 await page.locator('#notes-button').click();assert.equal(await page.locator('#notes-text section').count(),7);
 await page.reload();assert.ok((await page.locator('#status').textContent()).startsWith('40 /'));
 await page.evaluate(()=>window.courseDeck.show(31));await page.locator('.slide.active .enlarge').click();assert.ok(await page.locator('#image-viewer').isVisible());await page.keyboard.press('Escape');
 const mobile=[];
 for(const width of [390,768,1024]){
  await page.setViewportSize({width,height:844});
  for(let i=0;i<64;i++){await page.evaluate(i=>window.courseDeck.show(i),i);const extra=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);if(extra>1)mobile.push({width,page:i+1,overflow:extra});}
 }
 const nojs=await browser.newPage({javaScriptEnabled:false});await nojs.goto('file://'+path.join(root,'week12/lecture/index.html'));report.no_js_slides=await nojs.locator('.slide:visible').count();await nojs.close();
 report.desktop_issues=issues;report.mobile_issues=mobile;report.errors=errors;report.slides=64;
 await fs.writeFile(path.join(out,'browser-receipt.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 if(issues.length||mobile.length||errors.length)process.exitCode=1;
 if(process.argv.includes('--pdf')){await page.setViewportSize({width:1500,height:930});await page.locator('#sample-n').evaluate(e=>{e.value='1200';e.dispatchEvent(new Event('input'));});await page.emulateMedia({media:'print'});await page.pdf({path:path.join(root,'output/pdf/12_week12_online_experiments.pdf'),printBackground:true,preferCSSPageSize:true});}
}finally{await browser.close();}
