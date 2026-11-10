import {chromium} from 'playwright';
import path from 'node:path';
import fs from 'node:fs/promises';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'output/validation/week11');
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,channel:'chrome'});
const errors=[],issues=[],report={};
try{
 const page=await browser.newPage({viewport:{width:1500,height:930},deviceScaleFactor:1});
 page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('file://'+path.join(root,'week11/lecture/index.html'));
 await page.evaluate(()=>document.fonts.ready);
 for(let i=0;i<76;i++){
  await page.evaluate(i=>window.courseDeck.show(i),i);
  const problem=await page.locator('.slide.active').evaluate(slide=>{
   const rect=slide.getBoundingClientRect(),footer=slide.querySelector('footer').getBoundingClientRect();
   const result=[];
   for(const el of slide.querySelectorAll('h1,h2,h3,p,pre,table,figure,.row,.flow,.roadmap')){
    const b=el.getBoundingClientRect();
    if(b.width===0||el.closest('footer'))continue;
    if(b.left<rect.left-1||b.right>rect.right+1||b.top<rect.top-1||b.bottom>footer.top-6)result.push({tag:el.tagName,cls:el.className,text:el.textContent.slice(0,60),box:{x:b.x,y:b.y,width:b.width,height:b.height},footer:footer.top});
    if(el.scrollWidth>el.clientWidth+2)result.push({tag:el.tagName,text:el.textContent.slice(0,40),scrollOverflow:el.scrollWidth-el.clientWidth});
   }
   return result;
  });
  if(problem.length)issues.push({page:i+1,issues:problem});
  await page.locator('.slide.active').screenshot({path:path.join(out,'slide-'+String(i+1).padStart(2,'0')+'.png')});
 }
 report.slide_count=await page.locator('.slide').count();
 await page.evaluate(()=>window.courseDeck.show(0));await page.keyboard.press('ArrowRight');
 if(!page.url().endsWith('#slide-2'))throw Error('keyboard navigation failed');
 await page.locator('#overview-button').click();await page.locator('[data-slide="33"]').click();
 if(!(await page.locator('#status').textContent()).startsWith('34 /'))throw Error('overview navigation failed');
 await page.locator('#metric-k').fill('4');await page.locator('#metric-k').dispatchEvent('input');
 if(!(await page.locator('#metric-live').textContent()).includes('Recall 1.00'))throw Error('interactive metric failed');
 await page.locator('#notes-button').click();if(!(await page.locator('#notes-panel').isVisible()))throw Error('notes failed');
 await page.reload();if(!(await page.locator('#status').textContent()).startsWith('34 /'))throw Error('hash resume failed');
 await page.evaluate(()=>window.courseDeck.show(53));
 await page.locator('.slide.active .enlarge').click();
 if(!(await page.locator('#image-viewer').isVisible()))throw Error('image zoom failed');
 await page.keyboard.press('Escape');
 if(await page.locator('#image-viewer').isVisible())throw Error('image escape failed');
 report.controls={keyboard:true,overview:true,metric_slider:true,notes:true,hash_resume:true,image_zoom:true};
 // Verify every slide at phone width, text flow rather than shrinking the whole deck.
 await page.setViewportSize({width:390,height:844});
 const mobile=[];
 for(let i=0;i<76;i++){
  await page.evaluate(i=>window.courseDeck.show(i),i);
  const extra=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  if(extra>1)mobile.push({page:i+1,overflow:extra});
 }
 report.mobile_document_overflow=mobile;
 await page.evaluate(()=>window.courseDeck.show(0));await page.screenshot({path:path.join(out,'mobile-cover.png'),fullPage:true});
 await page.setViewportSize({width:1500,height:930});
 // Reset interactive example to its printed k=3 condition.
 await page.locator('#metric-k').evaluate(e=>{e.value='3';e.dispatchEvent(new Event('input'));});
 await page.emulateMedia({media:'print'});
 await page.pdf({path:path.join(root,'output/pdf/11_week11_offline_evaluation.pdf'),printBackground:true,preferCSSPageSize:true});
 report.pdf_created=true;
 // Report is functional offline, handles empty filters, text escaping and details.
 await page.emulateMedia({media:'screen'});
 await page.goto('file://'+path.join(root,'week11/lab/sample/report.html'));
 await page.selectOption('#error','false_accept');const count=await page.locator('#rows button').count();
 if(count!==1)throw Error('expected one candidate false accept, got '+count);
 await page.locator('#rows button').click();if(!(await page.locator('#detail').isVisible()))throw Error('detail failed');
 await page.locator('#query').fill('NO_MATCH');if(!(await page.locator('#rows').textContent()).includes('없습니다'))throw Error('empty state failed');
 await page.locator('#reset').click();if(await page.locator('#rows button').count()!==24)throw Error('reset failed');
 report.report_controls={filter:true,details:true,empty:true,reset:true};
 // All content remains available without JavaScript.
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:1500,height:930}});
 await nojs.goto('file://'+path.join(root,'week11/lecture/index.html'));
 report.no_js_visible_slides=await nojs.locator('.slide:visible').count();await nojs.close();
 report.page_errors=errors;report.desktop_layout_issues=issues;
 await fs.writeFile(path.join(out,'browser-receipt.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report,null,2));
}finally{await browser.close();}
