import {chromium} from 'playwright';
import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import net from 'node:net';
const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'week10/lecture/assets');
const server=net.createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));const port=server.address().port;await new Promise(r=>server.close(r));
const proc=spawn(path.join(root,'.venv/bin/python'),['-m','uvicorn','week10.lab.app:app','--host','127.0.0.1','--port',String(port),'--no-access-log'],{cwd:root,env:{...process.env,WEEK10_RELEASE:'v1',WEEK10_LOG_STDOUT:'0',WEEK10_TIMEOUT_S:'0.25',WEEK10_CAPACITY:'2'},stdio:'ignore'});
let browser;
try{
 const base=`http://127.0.0.1:${port}`;
 for(let i=0;i<100;i++){try{if((await fetch(base+'/health/ready')).ok)break}catch{}await new Promise(r=>setTimeout(r,50));}
 browser=await chromium.launch({headless:true, executablePath:process.env.CHROMIUM_EXECUTABLE});const page=await browser.newPage({viewport:{width:1240,height:900},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(base);await page.waitForFunction(()=>document.querySelector('#manifest').children.length===4);
 await page.locator('#release').screenshot({path:path.join(out,'lab-release.png')});
 await page.locator('#send').click();await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('HTTP 200'));
 await page.locator('#result').screenshot({path:path.join(out,'lab-success.png')});
 await page.locator('#trace').screenshot({path:path.join(out,'lab-trace.png')});
 await page.selectOption('#scenario','slow');await page.locator('#send').click();await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('HTTP 504'));
 await page.locator('#trace').screenshot({path:path.join(out,'lab-timeout-trace.png')});
 await page.selectOption('#scenario','retrieval_error');await page.locator('#send').click();await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('HTTP 502'));
 await page.locator('#signals').screenshot({path:path.join(out,'lab-signals.png')});
 if(errors.length)throw Error(errors.join('\n'));
 // Verify updated standalone proposal form, save and reopen with input retained.
 await page.goto('file://'+path.join(root,'curriculum/2026-2/web/project-portfolio-week10.html'));
 await page.locator('textarea[data-field="author_roles"]').fill('합성 예시 팀 · 검증 담당');
 const downloadEvent=page.waitForEvent('download');await page.locator('[data-action="save"]').click();const download=await downloadEvent;
 const saved=path.join(root,'output/validation/week10/proposal-synthetic.html');await download.saveAs(saved);await page.goto('file://'+saved);
 if(await page.locator('textarea[data-field="author_roles"]').inputValue()!=='합성 예시 팀 · 검증 담당')throw Error('saved form lost content');
 if(!(await page.textContent('body')).includes('11월 7일'))throw Error('missing submission notice');
 await fs.writeFile(path.join(root,'output/validation/week10/browser-receipt.json'),JSON.stringify({screenshots:5,page_errors:errors,form_save_reopen:true,scope:'own local MOCK app and synthetic form only'},null,2));console.log('5 screenshots; no page errors; proposal save/reopen passed');
}finally{await browser?.close();proc.kill('SIGTERM');await new Promise(r=>proc.on('exit',r));}
