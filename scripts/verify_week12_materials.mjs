import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'output/validation/week12-materials');await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,channel:'chrome'}),errors=[];
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000},acceptDownloads:true});page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('file://'+path.join(root,'week12/assignment/index.html'));
 const text='B 보류. +9.02%p 개선이 있으나 p95 2868ms로 상한 1800ms 초과.';
 await page.locator('#decision').fill(text);await page.reload();assert.equal(await page.locator('#decision').inputValue(),text);
 await page.locator('#limits').fill('</textarea><script>window.INJECTED=true</script> 합성 데이터');
 const promise=page.waitForEvent('download');await page.locator('#save-html').click();const download=await promise;const file=path.join(out,download.suggestedFilename());await download.saveAs(file);
 await page.goto('file://'+file);assert.equal(await page.locator('#decision').inputValue(),text);assert.equal(await page.locator('#task').count(),0);assert.equal(await page.evaluate(()=>window.INJECTED),undefined);assert.ok((await page.locator('#limits').inputValue()).includes('<script>'));
 await page.locator('#limits').fill('교수 작성 합성 데이터이며 실제 제품 성과가 아님.');await page.locator('#api').fill('02번 요청 ID r-01, 배정 버전 확인. 같은 요청 재전송으로 중복 기록 없음.');await page.locator('#next').fill('B의 출력 길이를 줄인 뒤 같은 질문으로 정책 기간·비용·재고 조건·완결성을 검사.');await page.locator('#evidence').fill('A 1196명 55.02%, B 1204명 64.04%. 차이 +9.02%p, 95% 구간 [5.10, 12.91]%p.');
 await page.screenshot({path:path.join(out,'saved-memo.png'),fullPage:true});
 await page.evaluate(()=>document.body.classList.add('memo-print'));await page.emulateMedia({media:'print'});await page.pdf({path:path.join(out,'memo-print.pdf'),printBackground:true,preferCSSPageSize:true});await page.emulateMedia({media:'screen'});
 const mobile=[];for(const target of ['week12/assignment/index.html','week12/lab/sample/report.html','week12/lecture/instructor/index.html']){await page.goto('file://'+path.join(root,target));await page.setViewportSize({width:390,height:844});const extra=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);if(extra>1)mobile.push({target,extra});}
 await page.setViewportSize({width:1440,height:1000});await page.goto('file://'+path.join(root,'week12/lab/sample/report.html'));
 for(const [scenario,expected] of [['healthy','REVIEW'],['slow','HOLD'],['srm','INVALID']]){await page.selectOption('#scenario',scenario);assert.equal(await page.locator('#decision').textContent(),expected);if(scenario==='srm'){assert.equal(await page.locator('#lift').textContent(),'해석 중단');assert.equal(await page.locator('#interval svg').count(),0);}}
 const data=JSON.parse(await fs.readFile(path.join(root,'week12/lab/sample/results.json'),'utf8'));
 const dl=page.waitForEvent('download');await page.locator('#download').click();const result=await dl;const saved=path.join(out,'case.json');await result.saveAs(saved);const parsed=JSON.parse(await fs.readFile(saved,'utf8'));assert.deepEqual(parsed,data.srm);
 const report={assignment_save_reload:true,standalone_memo:true,escaped_text:true,report_scenarios:true,raw_json:true,mobile_issues:mobile,page_errors:errors};await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify(report,null,2));console.log(report);assert.equal(mobile.length,0);assert.equal(errors.length,0);
}finally{await browser.close();}
