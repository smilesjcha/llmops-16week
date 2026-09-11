/** Week 02 editable lecture deck. Build runtime details: see BUILD.md. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
import {renderTeachingVisual} from './visual_layouts.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SKILL = process.env.PRESENTATIONS_SKILL_DIR;
const PYTHON = process.env.ARTIFACT_PYTHON;
if (!SKILL || !PYTHON) throw new Error('Set PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON; see BUILD.md');
const revision = process.env.DECK_REVISION || 'v1';
const BUILD = path.join(HERE, 'build', revision);
await fs.mkdir(BUILD, {recursive:true});
const content = JSON.parse(await fs.readFile(path.join(HERE, 'slide_content.json'), 'utf8'));
const specs = Array.isArray(content) ? content : content.slides;
const captureSpecs = JSON.parse(await fs.readFile(path.join(HERE,'assets','captures.json'),'utf8')).images;
const externalFigures = JSON.parse(await fs.readFile(path.join(HERE,'assets','external','figures.json'),'utf8'));
const measuredRun = JSON.parse(await fs.readFile(path.join(HERE,'assets','ollama-results-summary.json'),'utf8'));
const pictureCrops = [];
const C = {black:'#050505', ink:'#191919', white:'#FFFFFF', paper:'#F7F8FA', navy:'#0B1F3A', blue:'#2563EB', soft:'#E0F0FE', gray:'#667085', line:'#D0D5DD', darkLine:'#314156', muted:'#AFB8C7'};
const FONT='AppleGothic', MONO='Menlo';
const p = Presentation.create({slideSize:{width:1280,height:720}});
p.theme.colorScheme = {name:'BLACK WHITE NAVY BLUE',themeColors:{accent1:C.blue,accent2:C.navy,accent3:C.gray,accent4:C.soft,accent5:C.ink,accent6:C.line,bg1:C.white,bg2:C.black,tx1:C.ink,tx2:C.white,dk1:C.black,dk2:C.navy,lt1:C.white,lt2:C.paper,hlink:C.blue,folHlink:C.navy}};
const boxes=[], tableOwners=[], chartOwners=[], minSizes=[], layoutNames=[], renderErrors=[];
let current=0;
const plain=s=>String(s??'').replace(/\*\*/g,'').replace(/`/g,'');
const advance=(s,px,mono=false)=>[...s].reduce((a,c)=>a+(/[\u2e80-\uffff]/.test(c)?1:(mono?0.61:/[MW@]/.test(c)?0.83:/[il .,:'!|]/.test(c)?0.28:0.55))*px,0);
function wrap(text,width,pt,mono=false){
  return plain(text).split('\n').flatMap(line=>{
    if(advance(line,pt*4/3,mono)<=width) return [line];
    const words=line.split(/\s+/), lines=[];let carry='';
    for(const word of words){
      const next=carry?`${carry} ${word}`:word;
      if(carry&&advance(next,pt*4/3,mono)>width){lines.push(carry);carry=word;}else carry=next;
    }
    if(carry)lines.push(carry);return lines;
  }).join('\n');
}
function rect(s,x,y,w,h,fill,line='none',lineWidth=0){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:line,width:lineWidth,style:'solid'}});}
function rule(s,x,y,w,color=C.line,width=1){return rect(s,x,y,w,width,color);}
function txt(s,value,x,y,w,h,pt=20,opts={}){
  if(pt<14)throw new Error(`Below 14pt at slide ${current}`);
  minSizes.push(pt);
  const value2=opts.noWrap?plain(value):wrap(value,w,pt,opts.mono);
  const lines=value2.split('\n');
  const estimated=lines.length*pt*4/3*(opts.leading??1.2);
  if(estimated>h+3)throw new Error(`Text height ${current}: ${estimated.toFixed(0)}>${h}: ${value2}`);
  if(lines.some(l=>advance(l,pt*4/3,opts.mono)>w+6))throw new Error(`Text width ${current}: ${value2}`);
  const b=rect(s,x,y,w,h,'none');b.text=value2;
  b.text.style={fontSize:pt*4/3,typeface:opts.mono?MONO:FONT,bold:opts.bold??false,color:opts.color??C.ink,alignment:opts.align??'left',verticalAlignment:'top',lineSpacing:opts.leading??1.2,autoFit:'none',wrap:'none',insets:{top:0,right:0,bottom:0,left:0}};
  boxes.push({slide:current,x,y,w,h,text:value2,pt});return b;
}
function textHeight(value,w,pt=20){return wrap(value,w,pt).split('\n').length*pt*4/3*1.2+4;}
function shell(s,spec,dark=false){
  const fg=dark?C.white:C.ink,muted=dark?C.muted:C.gray;s.background.fill=dark?C.black:C.paper;
  txt(s,`W02 / ${spec.section}`,64,28,1030,26,14,{color:muted});
  txt(s,String(current).padStart(2,'0'),1140,28,76,26,14,{color:muted,mono:true,align:'right'});
  txt(s,spec.title,64,76,1152,80,38,{color:fg,bold:true});
  rule(s,64,666,1152,dark?C.darkLine:C.line);
  txt(s,'LLMOPS · 통합 강좌 · 프롬프트 설계와 버전 관리',64,680,1152,25,14,{color:muted});
  return {fg,muted,dark};
}
function list(s,items,x,y,w,pt=20,opts={}){
  for(const item of items??[]){const h=textHeight(item,w,pt);txt(s,item,x,y,w,h,pt,opts);y+=h+(opts.gap??22);}
  if(y-(opts.gap??22)>646)throw new Error(`Body overflow on ${current}`);return y;
}
function intro(s,spec,colors,maxWidth=1152){
  if(!spec.kicker)return 180;
  const h=textHeight(spec.kicker,maxWidth,18);txt(s,spec.kicker,64,168,maxWidth,h,18,{color:colors.muted});return 168+h+24;
}
function cover(s,spec){
  s.background.fill=C.black;
  txt(s,'W02 / INTEGRATED LLMOPS COURSE',64,42,1100,26,14,{color:C.muted});
  txt(s,'프롬프트 설계',64,156,1152,100,58,{color:C.white,bold:true});
  txt(s,'버전 관리',64,265,1152,100,58,{color:C.white,bold:true});
  rule(s,64,407,1152,C.darkLine);
  txt(s,spec.kicker||'명확한 지시 · 출력 기준 · 비교 실험',64,449,1152,82,24,{color:C.white});
  list(s,spec.body,64,520,1152,18,{color:C.muted,gap:8});
}
function section(s,spec){
  s.background.fill=spec.n%2?C.navy:C.black;
  txt(s,`W02 / ${spec.section}`,64,40,1050,26,14,{color:C.muted});
  txt(s,String(current).padStart(2,'0'),1134,40,82,26,14,{color:C.muted,mono:true,align:'right'});
  txt(s,spec.title,64,195,1152,160,46,{color:C.white,bold:true});
  rule(s,64,420,1152,C.darkLine);
  list(s,spec.body,64,467,1130,22,{color:C.white,gap:16});
}
function statement(s,spec){
  const colors=shell(s,spec,current%3===0);let y=intro(s,spec,colors);
  const items=spec.body??[];
  if(items.length){const h=textHeight(items[0],1120,30);txt(s,items[0],64,y+28,1120,h,30,{bold:true,color:colors.fg});y+=h+92;}
  rule(s,64,y-24,1152,colors.dark?C.darkLine:C.line);
  list(s,items.slice(1),64,y+12,1100,20,{color:colors.muted,gap:22});
}
function compare(s,spec){
  const colors=shell(s,spec);const y=intro(s,spec,colors);
  const columns=spec.columns??(spec.body??[]).map(v=>({heading:v,body:[]}));
  const width=(1152-40*(columns.length-1))/columns.length;
  columns.forEach((col,i)=>{
    const x=64+i*(width+40);const hh=textHeight(col.heading,width,25);
    txt(s,col.heading,x,y+14,width,hh,25,{bold:true});rule(s,x,y+hh+37,width,C.ink);
    list(s,col.body,x,y+hh+62,width,19,{color:C.gray,gap:24});
  });
  if(spec.columns&&spec.body?.length)list(s,spec.body,64,572,1152,18,{gap:12});
}
function steps(s,spec){
  const colors=shell(s,spec);const y=intro(s,spec,colors);const items=spec.steps??(spec.body??[]).map(v=>({title:v,detail:''}));
  if(items.length<=3&&current%2===0){
    const w=(1152-48*(items.length-1))/items.length;
    items.forEach((it,i)=>{const x=64+i*(w+48);txt(s,String(i+1).padStart(2,'0'),x,y+12,w,66,36,{mono:true,color:C.gray});rule(s,x,y+104,w);const h=textHeight(it.title,w,25);txt(s,it.title,x,y+140,w,h,25,{bold:true});list(s,[it.detail].filter(Boolean),x,y+162+h,w,19,{color:C.gray});});
  }else{
    const total=items.reduce((a,it)=>a+Math.max(textHeight(it.title,350,23),textHeight(it.detail??'',700,19))+36,0);
    if(y+total>646)throw new Error(`Steps overflow ${current}`);
    let yy=y;
    items.forEach((it,i)=>{const h=Math.max(textHeight(it.title,340,23),textHeight(it.detail??'',690,19));txt(s,String(i+1).padStart(2,'0'),64,yy+5,62,40,20,{mono:true,color:C.gray});txt(s,it.title,152,yy,330,h,23,{bold:true});if(it.detail)txt(s,it.detail,526,yy,690,h,19,{color:C.gray});rule(s,152,yy+h+18,1064);yy+=h+36;});
  }
}
function table(s,spec){
  const colors=shell(s,spec);const y=intro(s,spec,colors);const rows=spec.rows;
  if(!rows?.length){steps(s,spec);return;}
  const n=rows[0].length;
  const widths=spec.columnWidths??(n===2?[340,812]:n===3?[240,440,472]:[170,...Array(n-1).fill(982/(n-1))]);
  const font=17;
  const values=rows.map(row=>row.map((v,i)=>wrap(v,widths[i]-32,font)));
  const heights=values.map(row=>Math.max(...row.map(v=>v.split('\n').length))*font*4/3*1.18+24);
  const height=heights.reduce((a,b)=>a+b,0);
  if(y+height>630)throw new Error(`Table overflow ${current}: ${y}+${height}`);
  const t=s.tables.add({rows:rows.length,columns:n,left:64,top:y,width:1152,height,columnWidths:widths,values});
  t.styleOptions={headerRow:false,bandedRows:false};
  t.borders.assign({fill:C.line,width:1,style:'solid'});
  values.forEach((row,r)=>{t.rows[r].height=heights[r];row.forEach((_,c)=>{const cell=t.getCell(r,c);cell.fill=r===0?C.ink:C.white;cell.text.style={fontSize:font*4/3,typeface:FONT,color:r===0?C.white:C.ink,bold:r===0,autoFit:'none',wrap:'none',verticalAlignment:'middle',insets:{left:16,right:16,top:12,bottom:12}};});});
  tableOwners.push(current);minSizes.push(font);
  if(spec.body?.length)list(s,spec.body,64,y+height+24,1152,18,{color:C.gray,gap:10});
}
function code(s,spec){
  const colors=shell(s,spec);let y=intro(s,spec,colors);
  // Includes exporter/Impress paragraph baselines and authored blank lines.
  const code=spec.code??'';const h=code.split('\n').length*16*4/3*1.5+56;
  if(y+h>628)throw new Error(`Code overflow ${current}`);
  rect(s,64,y,1152,h,C.navy);txt(s,code,88,y+24,1104,h-48,16,{mono:true,color:C.white,noWrap:true});
  if(spec.body?.length)list(s,spec.body,64,y+h+24,1152,18,{color:C.gray,gap:14});
}
async function screenshot(s,spec){
  const colors=shell(s,spec);const y=intro(s,spec,colors);const filename=spec.screenshot;
  const file=path.join(HERE,'assets',filename);
  const bytes=new Uint8Array(await fs.readFile(file));
  const capture=captureSpecs[filename];
  if(!capture)throw new Error(`Missing source/crop evidence: ${filename}`);
  const [sw,sh]=capture.size,[rx,ry,rw,rh]=capture.region;
  const scale=Math.min(1152/rw,(500-y)/rh);
  const frame={left:64+(1152-rw*scale)/2,top:y+(500-y-rh*scale)/2,width:rw*scale,height:rh*scale};
  const crop={left:rx/sw,top:ry/sh,right:(sw-rx-rw)/sw,bottom:(sh-ry-rh)/sh};
  s.images.add({blob:bytes,contentType:'image/jpeg',alt:spec.caption||spec.title,fit:'cover',crop,position:frame});
  pictureCrops.push({slide:current,filename,crop:{l:crop.left,t:crop.top,r:crop.right,b:crop.bottom},frame});
  const items=spec.body??[];const w=(1152-36*(items.length-1))/Math.max(1,items.length);
  items.forEach((item,i)=>{const x=64+i*(w+36);txt(s,String(i+1).padStart(2,'0'),x,522,w,28,14,{color:C.gray,mono:true});txt(s,item,x,560,w,64,18,{color:C.ink});});
}
async function externalPicture(s,key,position,pictureIndex=0,pictureCount=1){
  const item=externalFigures[key];if(!item)throw new Error(`Unknown external figure ${key}`);
  const [sw,sh]=item.size,[x,y,w,h]=item.region;
  const scale=Math.min(position.width/w,position.height/h);
  const frame={left:position.left+(position.width-w*scale)/2,top:position.top+(position.height-h*scale)/2,width:w*scale,height:h*scale};
  const crop={left:x/sw,top:y/sh,right:(sw-x-w)/sw,bottom:(sh-y-h)/sh};
  const blob=new Uint8Array(await fs.readFile(path.join(HERE,'assets','external',item.file)));
  s.images.add({blob,contentType:item.file.endsWith('.png')?'image/png':'image/jpeg',alt:key,fit:'cover',crop,position:frame});
  pictureCrops.push({slide:current,filename:item.file,pictureIndex,pictureCount,crop:{l:crop.left,t:crop.top,r:crop.right,b:crop.bottom},frame});
}
async function researchVisual(s,spec){
  const v=spec.visual;
  if(spec.layout==='photo-study'){
    await externalPicture(s,'apple-blank',{left:64,top:207,width:320,height:320},0,2);
    await externalPicture(s,'apple-ipod',{left:424,top:207,width:320,height:320},1,2);
    txt(s,'사과 85.61%',64,554,320,46,25,{bold:true});
    txt(s,'iPod 99.68%',424,554,320,46,25,{bold:true});
    txt(s,v.question,808,207,408,143,26,{bold:true});
    txt(s,v.model,808,381,408,42,24,{bold:true});
    txt(s,'Contrastive Language–Image\nPre-training',808,432,408,61,16,{color:C.gray});
    txt(s,v.limitation,808,515,408,81,17,{color:C.gray});
    txt(s,'사진별 분류 점수 · 검증된 정확도나 신뢰도가 아님',64,606,1152,28,14,{color:C.gray});
    return;
  }
  if(v.asset==='demonstrations'){
    await externalPicture(s,'demonstrations',{left:64,top:215,width:744,height:334});
    txt(s,v.heading,871,224,345,119,27,{bold:true});
    txt(s,v.takeaway,871,386,345,98,22);
    txt(s,v.limitation,64,579,1152,39,19,{color:C.gray});
  }else if(v.asset==='lost-middle'){
    await externalPicture(s,'lost-middle',{left:64,top:181,width:455,height:435});
    txt(s,v.heading,592,205,624,47,26,{bold:true});
    txt(s,v.takeaway,592,282,624,95,27,{bold:true});
    txt(s,'실습에서 고정할 조건',592,421,624,42,22,{bold:true});
    txt(s,'입력 내용과 순서\n모델과 생성 설정',592,482,624,87,22,{color:C.gray});
    txt(s,v.limitation,592,588,624,39,14,{color:C.gray});
  }else if(v.asset==='tot'){
    await externalPicture(s,'tot-chain',{left:64,top:181,width:320,height:417},0,2);
    await externalPicture(s,'tot-tree',{left:403,top:181,width:385,height:417},1,2);
    txt(s,v.heading,837,213,379,91,27,{bold:true});
    txt(s,v.takeaway,837,354,379,103,22);
    txt(s,'CoT: Chain of Thought\nToT: Tree of Thoughts',837,490,379,76,17,{color:C.gray});
    txt(s,v.limitation,64,605,1152,29,14,{color:C.gray});
  }else throw new Error(`Unknown research asset ${v.asset}`);
}
function measuredChart(s,spec){
  const v=spec.visual;
  txt(s,v.heading,64,181,1152,43,24,{bold:true});
  s.charts.add('bar',{
    position:{left:64,top:257,width:744,height:331},
    categories:measuredRun.categories,
    series:[{name:'전체 검사 통과',values:measuredRun.overall_pass_counts,fill:C.navy}],
    hasLegend:false,barOptions:{direction:'column',grouping:'clustered',gapWidth:120},
    chartFill:C.paper,plotAreaFill:C.paper,chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0},
    xAxis:{visible:true,textStyle:{typeface:FONT,fontSize:24,fill:C.ink},majorGridlines:null,line:{fill:C.gray,width:1}},
    yAxis:{visible:true,min:0,max:3,majorUnit:1,numberFormatCode:'0',textStyle:{typeface:FONT,fontSize:20,fill:C.gray},majorGridlines:{fill:C.line,width:1},line:{fill:'none',width:0}},
    dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:FONT,fontSize:30,fill:C.ink,bold:true}},
  });
  chartOwners.push(current);minSizes.push(15);
  txt(s,'qwen3:4b-instruct',862,264,354,38,18,{mono:true,bold:true});
  txt(s,'T01 · T03 · T07\n같은 문의 3건씩',862,325,354,86,21,{color:C.gray});
  txt(s,v.takeaway,862,441,354,146,20,{bold:true});
  txt(s,v.limitation,64,607,1152,28,14,{color:C.gray});
}
function caseLayout(s,spec){
  const colors=shell(s,spec);const y=intro(s,spec,colors);
  if(spec.columns){compare(s,spec);return;}
  const body=spec.body??[];
  const h=Math.max(120,textHeight(body[0]??'',1080,26)+48);
  rect(s,64,y,1152,h,C.white);txt(s,body[0]??'',96,y+24,1080,h-48,26,{bold:true});
  list(s,body.slice(1),64,y+h+36,1152,20,{gap:20});
}
function worksheet(s,spec){
  if(spec.rows)return table(s,spec);
  const colors=shell(s,spec);let y=intro(s,spec,colors);
  for(const [i,v] of (spec.body??[]).entries()){
    txt(s,String(i+1).padStart(2,'0'),64,y,60,34,18,{mono:true,color:C.gray});const h=textHeight(v,1040,21);
    txt(s,v,152,y,1040,h,21);rule(s,152,y+h+22,1064);y+=h+52;
  }
  if(y>668)throw new Error(`Worksheet overflow ${current}`);
}
function roadmap(s,spec){
  const colors=shell(s,spec);const entries=spec.rows.slice(1);
  // Eight weeks in a 2-column editorial rail, each with date/topic/mode.
  entries.forEach((row,i)=>{
    const x=64+Math.floor(i/4)*590,y=178+(i%4)*103,w=562;
    const active=Number(row[0].slice(0,2))===spec.currentWeek;
    if(active)rect(s,x,y,w,92,C.soft);
    txt(s,row[0],x+16,y+10,190,26,14,{mono:true,color:active?C.blue:C.gray,bold:active});
    txt(s,row[2],x+222,y+10,324,26,14,{align:'right',color:active?C.blue:C.gray,bold:active});
    txt(s,row[1],x+16,y+48,530,36,20,{bold:true,color:active?C.blue:C.ink});
    if(!active)rule(s,x,y+93,w);
  });
  txt(s,spec.body.join(' / '),64,617,1152,42,14,{color:colors.muted});
}
for(const [i,spec] of specs.entries()){
  current=i+1;
  if(spec.n!==current)throw new Error(`Slide sequence mismatch ${current}`);
  if(!spec.notes||!spec.sources?.length)throw new Error(`Notes/sources missing ${current}`);
  if(i>=2&&spec.layout===specs[i-1].layout&&spec.layout===specs[i-2].layout)throw new Error(`Repeated layout ${current}`);
  const s=p.slides.add();layoutNames.push(spec.layout);
  try { if(spec.visual){
    shell(s,spec);
    if(spec.layout==='photo-study'||spec.layout==='research-figure')await researchVisual(s,spec);
    else if(spec.layout==='result-chart')measuredChart(s,spec);
    else if(!renderTeachingVisual(s,spec,{txt,rect,rule,C,FONT,registerTable:n=>tableOwners.push(n)}))throw new Error(`Unknown visual ${spec.layout}`);
  } else switch(spec.layout){
    case 'cover':cover(s,spec);break;case 'section':section(s,spec);break;
    case 'statement':statement(s,spec);break;case 'compare':compare(s,spec);break;
    case 'steps':steps(s,spec);break;case 'table':table(s,spec);break;
    case 'agenda':spec.rows?table(s,spec):steps(s,spec);break;
    case 'timeline':spec.rows?table(s,spec):steps(s,spec);break;
    case 'roadmap':roadmap(s,spec);break;case 'code':code(s,spec);break;
    case 'screenshot':await screenshot(s,spec);break;case 'worksheet':worksheet(s,spec);break;
    case 'case':caseLayout(s,spec);break;default:throw new Error(`Unknown layout ${spec.layout}`);
  } } catch (error) {renderErrors.push(`${current}: ${error.message}`);}
  if(spec.caption)txt(s,spec.caption,64,635,1152,28,14,{color:C.gray});
  const licenseNotice=spec.visual?.asset==='tot'?`\n\n[Image license]\n${await fs.readFile(path.join(HERE,'assets','external','tree-of-thoughts-LICENSE.txt'),'utf8')}`:'';
  s.speakerNotes.textFrame.setText(`${spec.notes}\n\n[Sources]\n${spec.sources.map(v=>`- ${v}`).join('\n')}\n[/Sources]${licenseNotice}`);
  s.speakerNotes.setVisible(true);
}
if(renderErrors.length)throw new Error(renderErrors.join('\n'));
await fs.writeFile(path.join(BUILD,'geometry.json'),JSON.stringify(boxes,null,2));
await fs.writeFile(path.join(BUILD,'manifest.json'),JSON.stringify({slides:specs.length,minFontPt:Math.min(...minSizes),tableOwners,chartOwners,layouts:layoutNames,palette:C},null,2));
const candidate=path.join(BUILD,'candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
// This runtime substitutes center-fit crops during export. Restore the authored
// native source rectangles before structural validation, import, and PDF QA.
const cropManifest=path.join(BUILD,'picture-crops.json');
await fs.writeFile(cropManifest,JSON.stringify(pictureCrops,null,2));
execFileSync(PYTHON,[path.join(HERE,'repair_picture_crops.py'),candidate,cropManifest],{stdio:'inherit'});
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(BUILD,'final','02_week2_prompt_design_versioning.pptx');
await fs.mkdir(path.dirname(finalPath),{recursive:true});
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,explicitTotalSlideCount:72,requiredNativeTableOwnerSlides:tableOwners,requiredNativeChartOwnerSlides:chartOwners,materializeLiteralChartWorkbooks:chartOwners.length>0,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:[FONT,MONO]},verifyArtifactToolImport:true,receiptPath:path.join(BUILD,'validation.json')});
console.log(JSON.stringify({finalPath,slides:specs.length,minFontPt:Math.min(...minSizes),nativeTables:tableOwners,layouts:[...new Set(layoutNames)]}));
