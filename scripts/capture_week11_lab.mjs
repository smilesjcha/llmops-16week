import {chromium} from 'playwright';
import path from 'node:path';
import fs from 'node:fs/promises';
const root=path.resolve(import.meta.dirname,'..');
const browser=await chromium.launch({headless:true,channel:'chrome'});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1040},deviceScaleFactor:1});
 await page.goto('file://'+path.join(root,'week11/lab/sample/report.html'));
 await page.locator('#comparison tbody tr').first().waitFor();
 await page.screenshot({path:path.join(root,'week11/lecture/assets/lab-report.png')});
 await page.locator('.metrics').screenshot({path:path.join(root,'week11/lecture/assets/lab-report-metrics.png')});
 await page.locator('.filters').screenshot({path:path.join(root,'week11/lecture/assets/lab-report-filters.png')});
 await page.selectOption('#error','false_accept');
 await page.locator('#rows button').first().click();
 await page.locator('#detail').screenshot({path:path.join(root,'week11/lecture/assets/lab-error-detail.png')});
 console.log('Captured actual offline report and error detail');
}finally{await browser.close();}
