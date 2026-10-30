import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {decks} from './course_deck_content.mjs';
import {week09Renderers} from './week09_renderers.mjs';
import {C as BaseColors,FONT,MONO,CANVAS,resolveLayout,auditDeck} from './presentation_design.mjs';
const ROOT=path.resolve(import.meta.dirname,'..');
const week=Number(process.argv[2]); const D=decks[week];
const C=[6,7,9].includes(week)?{...BaseColors,green:'#284B72',soft:'#EDF1F6'}:BaseColors;
if(!D)throw Error('Usage: node scripts/build_course_deck.mjs 4|5|6|7|8|9');
const noPublish=process.argv.includes('--no-publish');
const SKILL=process.env.PRESENTATIONS_SKILL_DIR, PY=process.env.ARTIFACT_PYTHON;
if(!SKILL||!PY)throw Error('Bundled runtime variables required');
const BUILD=path.join(ROOT,`week${String(week).padStart(2,'0')}/lecture/build`);
await fs.mkdir(BUILD,{recursive:true});
const p=Presentation.create({slideSize:{width:CANVAS.width,height:CANVAS.height}});
p.theme.colorScheme={name:'LLMOPS EDITORIAL',themeColors:{accent1:C.green,accent2:C.navy,accent3:C.gray,accent4:C.soft,accent5:C.ink,accent6:C.line,bg1:C.white,bg2:C.black,tx1:C.ink,tx2:C.white,dk1:C.black,dk2:C.navy,lt1:C.white,lt2:C.paper,hlink:C.green,folHlink:C.navy}};
let current=0;const geometry=[];
const advance=(v,px,mono=false)=>[...String(v)].reduce((s,c)=>s+(/[^\x00-\x7F]/.test(c)?px:mono?px*.61:/[MW@]/.test(c)?px*.82:/[il .,:'!|]/.test(c)?px*.28:px*.55),0);
const wrap=(v,w,pt,mono=false)=>String(v).split('\n').flatMap(line=>{const out=[];let carry='';for(const word of line.split(/\s+/)){if(advance(word,pt*4/3,mono)>w+2)throw Error(`Unbreakable word s${current}: ${word}`);const next=carry?carry+' '+word:word;if(carry&&advance(next,pt*4/3,mono)>w){out.push(carry);carry=word}else carry=next}out.push(carry);return out}).join('\n');
const h=(v,w,pt=20)=>wrap(v,w,pt).split('\n').length*pt*4/3*1.16+3;
function rect(s,x,y,w,ht,fill='none',stroke='none',sw=0){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:ht},fill,line:{fill:stroke,width:sw,style:'solid'}})}
function rule(s,x,y,w,color=C.line){rect(s,x,y,w,1,color)}
function text(s,v,x,y,w,ht,pt=20,o={}){const val=o.mono?String(v):wrap(v,w,pt); if(pt<14||y<0||y+ht>720||x<0||x+w>1280)throw Error(`Geometry s${current} ${v}`);if(val.split('\n').length*pt*4/3*1.16>ht+4)throw Error(`Text height s${current} ${val}`);const box=rect(s,x,y,w,ht);box.text=val;box.text.style={typeface:o.mono?MONO:FONT,fontSize:pt*4/3,color:o.color||C.ink,bold:!!o.bold,alignment:o.align||'left',verticalAlignment:'top',wrap:'none',autoFit:'none',lineSpacing:1.16,insets:{top:0,bottom:0,left:0,right:0}};geometry.push({slide:current,x,y,w,h:ht,text:val,pt});return box}
function list(s,items,x,y,w,pt=20,o={}){for(const item of items){const ht=h(item,w,pt);text(s,item,x,y,w,ht,pt,o);y+=ht+(o.gap??20)}return y}
function shell(s,a){s.background.fill=C.paper;text(s,`LLMOPS / W${String(week).padStart(2,'0')}`,64,26,1000,24,14,{color:C.gray});text(s,String(current).padStart(2,'0'),1140,26,76,24,14,{mono:true,color:C.gray,align:'right'});text(s,a.title,64,76,1152,70,34,{bold:true});rule(s,64,663,1152);text(s,D.subtitle,64,680,1152,24,14,{color:C.gray})}
function note(s,a){if(a.caption)text(s,a.caption,64,608,1152,48,16,{color:C.gray})}
function cover(s,a){s.background.fill=C.black;text(s,`LLMOPS / WEEK ${String(week).padStart(2,'0')}`,64,42,1100,24,14,{color:C.muted});text(s,a.title,64,174,1152,200,54,{bold:true,color:C.white});rule(s,64,426,1152,C.gray);list(s,a.items,64,464,1120,20,{color:C.muted,gap:16})}
function section(s,a){s.background.fill=C.navy;text(s,`W${String(week).padStart(2,'0')} / ${String(current).padStart(2,'0')}`,64,42,1100,24,14,{color:C.muted});text(s,a.title,64,176,1152,160,44,{bold:true,color:C.white});rule(s,64,392,1152,C.gray);list(s,a.items,64,440,1152,23,{color:C.white,gap:18})}
function statement(s,a){shell(s,a);text(s,a.items[0],64,208,1110,h(a.items[0],1110,30),30,{bold:true});list(s,a.items.slice(1),64,398,1110,22,{color:C.gray,gap:24});note(s,a)}
function focus(s,a){shell(s,a);const main=a.items[0];text(s,main,64,212,1090,172,43,{bold:true});rule(s,64,405,600,C.green);list(s,a.items.slice(1),64,446,1080,22,{color:C.gray,gap:20});note(s,a)}
function annotated(s,a){shell(s,a);rect(s,64,192,738,380,C.navy);text(s,a.items[0],92,220,682,324,18,{mono:true,color:C.white});text(s,a.items[1],846,220,360,110,24,{bold:true});rule(s,846,352,360,C.green);list(s,a.items.slice(2),846,379,360,19,{color:C.gray,gap:17});note(s,a)}
function compare(s,a){shell(s,a);a.items.forEach(([head,...items],i)=>{const x=64+i*596;text(s,head,x,216,556,84,29,{bold:true});rule(s,x,315,556,i?C.gray:C.green);list(s,items,x,354,550,23,{color:C.gray,gap:42})});note(s,a)}
function steps(s,a){shell(s,a);const count=a.items.length,slot=390/count;for(const [i,[head,body]] of a.items.entries()){const y=192+i*slot,ht=Math.max(h(head,300,23),h(body,700,21));text(s,String(i+1).padStart(2,'0'),64,y+2,60,34,18,{mono:true,color:C.green});text(s,head,146,y,315,ht,23,{bold:true});text(s,body,502,y,712,ht,21,{color:C.gray});rule(s,146,y+ht+14,1070)}note(s,a)}
function flow(s,a){shell(s,a);const count=a.items.length,w=1152/count;rule(s,64,285,1152,C.line);a.items.forEach((item,i)=>{const x=64+i*w,[head,detail]=Array.isArray(item)?item:[item,null];rect(s,x,279,16,13,C.green);text(s,String(i+1).padStart(2,'0'),x,220,w-20,32,18,{mono:true,color:C.green});text(s,head,x,322,w-26,104,25,{bold:true});if(detail)text(s,detail,x,423,w-26,96,18,{color:C.gray})});note(s,a)}
function swimlane(s,a){shell(s,a);a.items.forEach(([label,...nodes],row)=>{const y=210+row*186;text(s,label,64,y+34,138,44,23,{bold:true});const boxes=[];nodes.forEach((node,i)=>{const x=240+i*328;const box=rect(s,x,y,290,124,C.white,C.line,1);text(s,node,x+18,y+36,254,74,21,{bold:true});boxes.push(box)});for(let i=1;i<boxes.length;i++)s.shapes.connect(boxes[i-1],boxes[i],{kind:'straight',fromSide:'right',toSide:'left',line:{fill:C.gray,width:2},tail:{type:'triangle',width:'sm',length:'sm'}})});note(s,a)}
function table(s,a){shell(s,a);const rows=a.items,cols=rows[0].length;const widths=cols===2?[340,812]:cols===3?[300,492,360]:[410,350,196,196];const pt=rows.length<=5?19:17;const values=rows.map(r=>r.map((v,i)=>wrap(v,widths[i]-28,pt)));const minRow=Math.min(78,410/rows.length);const heights=values.map(r=>Math.max(minRow,Math.max(...r.map(v=>v.split('\n').length))*pt*4/3*1.16+24));const total=heights.reduce((x,y)=>x+y,0);if(total>410)throw Error(`Table overflow ${current}`);const t=s.tables.add({rows:rows.length,columns:cols,left:64,top:190,width:1152,height:total,columnWidths:widths,values});t.styleOptions={headerRow:false,bandedRows:false};let edge=190;rows.forEach((r,i)=>{t.rows[i].height=heights[i];r.forEach((_,j)=>{const cell=t.getCell(i,j);cell.fill=i===0?C.soft:C.white;for(const side of ['left','right','top','bottom']){cell.borders[side].visible=false;cell.borders[side].width=0;cell.borders[side].fill='none'}cell.text.style={typeface:FONT,fontSize:pt*4/3,color:i===0?C.navy:j===0?C.ink:C.gray,bold:i===0||j===0,wrap:'none',autoFit:'none',verticalAlignment:'middle',insets:{left:14,right:14,top:12,bottom:12}}});rule(s,64,edge,1152,i===0?C.navy:C.line);edge+=heights[i]});rule(s,64,edge,1152,C.navy);note(s,a)}
function caseLayout(s,a){shell(s,a);let y=190;for(const [i,v]of a.items.entries()){const pt=i===0?27:21;const ht=h(v,1100,pt);if(i===0)rule(s,64,y+ht+24,1152);text(s,v,64,y,1100,ht,pt,{bold:i===0,color:i===0?C.ink:C.gray});y+=ht+(i===0?68:32)}note(s,a)}
function code(s,a){shell(s,a);const lines=a.items.join('\n');const ht=lines.split('\n').length*18*4/3*1.22+70;if(lines.split('\n').some(v=>advance(v,24,true)>1100))throw Error(`Code width ${current}`);rect(s,64,208,1152,ht,C.navy);text(s,lines,90,240,1100,ht-60,18,{mono:true,color:C.white});note(s,a)}
function formula(s,a){shell(s,a);text(s,a.items[0],64,214,1152,110,28,{bold:true});rule(s,64,358,1152);list(s,a.items.slice(1),64,406,1120,22,{color:C.gray,gap:26});note(s,a)}
function tokenmap(s,a){
 shell(s,a);
 const values=[['예측 위치','0','1','2','3','4'],['입력 토큰','10','11','12','20','21'],['다음 정답','11','12','20','21','22'],['답변 학습','제외','제외','사용','사용','사용']];
 const t=s.tables.add({rows:4,columns:6,left:64,top:204,width:1152,height:328,columnWidths:[292,172,172,172,172,172],values});
 t.styleOptions={headerRow:false,bandedRows:false};
 for(let r=0;r<4;r++){t.rows[r].height=82;for(let c=0;c<6;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.soft:C.white;cell.text.style={typeface:FONT,fontSize:27,color:c===0?C.ink:C.gray,bold:c===0||r===0,alignment:c===0?'left':'center',verticalAlignment:'middle',insets:{left:18,right:18,top:16,bottom:16}};for(const side of ['top','bottom','left','right']){cell.borders[side].visible=false;cell.borders[side].fill='none';cell.borders[side].width=0}}rule(s,64,204+r*82,1152,r===0?C.navy:C.line)}
 rule(s,64,532,1152,C.navy);text(s,'원본 label의 3·4·5번 위치가 예측 2·3·4번 위치와 대응',64,557,1152,34,20,{color:C.gray});note(s,a);
}
function loraPaths(s,a){
 shell(s,a);
 const node=(x,y,w,head,body)=>{const box=rect(s,x,y,w,106,C.white,C.line,1);text(s,head,x+18,y+15,w-36,38,23,{bold:true});text(s,body,x+18,y+65,w-36,30,17,{color:C.gray});return box};
 const input=node(64,332,166,'입력 x','8 × 1');
 const fixed=node(340,202,430,'W 고정','12 × 8');
 const lowA=node(340,448,190,'A 학습','2 × 8');
 const lowB=node(588,448,182,'B 학습','12 × 2');
 const sum=node(998,332,218,'출력 합산','12 × 1');
 const connect=(from,to,kind='straight')=>s.shapes.connect(from,to,{kind,fromSide:'right',toSide:'left',line:{fill:C.blue,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});
 connect(input,fixed,'elbow');connect(input,lowA,'elbow');connect(lowA,lowB);connect(fixed,sum,'elbow');connect(lowB,sum,'elbow');
 text(s,'Wx',800,205,152,40,22,{bold:true});text(s,'(α/r)BAx',790,550,196,40,20,{color:C.gray});note(s,a);
}
function preferencePair(s,a){
 shell(s,a);
 const question=rect(s,300,180,680,82,C.white,C.line,1);
 text(s,'같은 질문 · 근거 문서가 없는 문의',324,204,632,42,23,{bold:true});
 const chosen=rect(s,64,350,548,166,C.white,C.line,1),rejected=rect(s,668,350,548,166,C.white,C.line,1);
 text(s,'chosen · 선택한 답변',88,370,500,40,23,{bold:true});
 text(s,'확인할 근거가 없어\n담당자 검토가 필요합니다.',88,430,500,70,21,{color:C.gray});
 text(s,'rejected · 선택하지 않은 답변',692,370,500,40,23,{bold:true});
 text(s,'무조건 승인됩니다.',692,430,500,70,21,{color:C.gray});
 for(const box of [chosen,rejected])s.shapes.connect(question,box,{kind:'elbow',fromSide:'bottom',toSide:'top',line:{fill:C.blue,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});
 text(s,'선택 기준: 근거 없는 단정 방지와 다음 행동 안내',64,552,1152,40,21,{color:C.gray});note(s,a);
}
function dpoPaths(s,a){
 shell(s,a);
 const node=(x,y,w,head,body)=>{const box=rect(s,x,y,w,108,C.white,C.line,1);text(s,head,x+18,y+15,w-36,38,23,{bold:true});text(s,body,x+18,y+65,w-36,32,18,{color:C.gray});return box};
 const input=node(64,330,208,'동일 입력','질문·답변 쌍');
 const policy=node(370,196,400,'policy · 학습','선호 차이: (−2)−(−5)=3');
 const reference=node(370,458,400,'reference · 고정','선호 차이: (−3)−(−3)=0');
 const margin=node(922,330,294,'차이의 차감','3 − 0 = 3');
 for(const target of [policy,reference])s.shapes.connect(input,target,{kind:'elbow',fromSide:'right',toSide:'left',line:{fill:C.blue,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});
 for(const source of [policy,reference])s.shapes.connect(source,margin,{kind:'elbow',fromSide:'right',toSide:'left',line:{fill:C.blue,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});
 note(s,a);
}
function windows(s,a){shell(s,a);text(s,'원본 문서 · 문자 위치',64,188,1080,38,22,{bold:true});rule(s,220,274,950,C.ink);for(const [i,[start,end]]of [[0,60],[48,108],[96,120]].entries()){const y=307+i*80,x=220+start*7.2,w=(end-start)*7.2;rect(s,x,y,w,52,i===1?C.soft:C.white,C.gray,1);text(s,`${start}–${end}`,x+12,y+13,w-24,28,16,{mono:true});text(s,`C${i+1}`,64,y+10,120,28,18,{mono:true})}text(s,a.items.join(' · '),64,573,1152,34,17,{color:C.gray});note(s,a)}
function dates(s,a){shell(s,a);a.items.forEach(([label,date,value],i)=>{const y=218+i*115;text(s,label,64,y,230,44,23,{bold:true});text(s,date,320,y,580,40,21,{color:C.gray});text(s,value,1040,y,176,44,23,{bold:true});rule(s,320,y+62,896)});note(s,a)}
function rank(s,a){shell(s,a);a.items.forEach(([label,body],i)=>{const y=212+i*113;text(s,label,64,y,220,38,23,{bold:true});text(s,body,300,y,890,74,22,{color:C.gray});rule(s,300,y+78,916)});note(s,a)}
function funnel(s,a){shell(s,a);a.items.forEach((item,i)=>{const w=1050-i*160,x=64+(1152-w)/2,y=186+i*96;rect(s,x,y,w,70,C.white,C.line,1);text(s,item,x+22,y+19,w-44,40,22)});note(s,a)}
function citation(s,a){shell(s,a);text(s,a.items[0],64,208,1152,94,27,{bold:true});rule(s,64,328,1152);list(s,a.items.slice(1),64,377,1120,22,{color:C.gray,gap:28});note(s,a)}
function ideas(s,a){shell(s,a);a.items.forEach(([head,detail],i)=>{const x=64+(i%2)*600,y=208+Math.floor(i/2)*204;text(s,head,x,y,550,70,27,{bold:true});rule(s,x,y+83,552);text(s,detail,x,y+112,550,74,21,{color:C.gray})});note(s,a)}
function roadmap(s,a){shell(s,a);const entries=[['01','09.04','실행 추적'],['02','09.11','프롬프트 비교'],['03','09.18','평가·오류 분류'],['04','09.25','RAG·근거 · 녹화'],['05','10.02','검색 품질'],['06','10.09','휴일 · 수업 없음'],['07','10.16','강의 재개·초안'],['08','10.23','기획서 평가 · 마감10.22'],['09–15','10.30–12.11','구현·운영·프로젝트'],['16','12.18','실시간 온라인 발표']];entries.forEach(([n,date,title],i)=>{const x=64+Math.floor(i/5)*594,y=179+(i%5)*86,active=Number(n)===week;if(active)rect(s,x,y,558,78,C.soft);text(s,n,x+12,y+10,90,23,14,{mono:true,color:active?C.blue:C.gray,bold:active});text(s,date,x+114,y+10,400,23,14,{color:C.gray});text(s,title,x+12,y+43,534,30,18,{bold:active,color:active?C.blue:C.ink})})}
for(const name of ['retrieval-chart-data.json','retrieval-timing.json']){
  await fs.access(path.join(ROOT,'output/validation',name)).catch(()=>execFileSync(PY,[path.join(ROOT,'scripts/measure_retrieval_charts.py')],{cwd:ROOT}));
}
const chartData=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/retrieval-chart-data.json'),'utf8'));
async function chart(s,a){shell(s,a);let categories,series,type='bar',format='0.0',max,majorUnit;
switch(a.chart){
case 'w9-stream':{const d=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week09-live/receipt.json'),'utf8')).stream_runs[0];categories=['첫 내용 조각','전체 완료'];series=[{name:'로컬 TCP · ms',values:[d.first_delta_ms,d.total_ms]}];format='0.0';break;}
case 'w9-errors':case 'w9-latency':case 'w9-goodput':case 'w9-cache':{const d=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week09-lab/benchmark-report.json'),'utf8'));categories=d.runs.map(x=>'동시 요청 '+x.concurrency);format='0.0';if(a.chart==='w9-errors'){series=[{name:'오류율',values:d.runs.map(x=>x.summary.error_rate)}];format='0.0%';max=1;}else if(a.chart==='w9-latency'){categories=d.runs.map(x=>'동시 '+x.concurrency+' (n='+x.summary.success+')');series=[50,95].map(p=>({name:'성공 p'+p+' · ms',values:d.runs.map(x=>x.summary.success_latency_ms['p'+p])}));max=Math.ceil(Math.max(...series.flatMap(x=>x.values))/10)*10;majorUnit=10;}else if(a.chart==='w9-goodput'){series=[{name:'성공 요청/s',values:d.runs.map(x=>x.summary.successful_rps)},{name:'전체 완료 요청/s',values:d.runs.map(x=>x.summary.completed_rps)}];}else{categories=['캐시 OFF','워밍업 후 적중'];series=[{name:'성공 p50 · ms',values:[d.runs[1].summary.success_latency_ms.p50,d.cached.summary.success_latency_ms.p50]}];}break;}
case 'dpo-beta':{const d=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week07-workshop/workshop-report.json'),'utf8'));type='line';categories=d.margins.map(String);series=d.beta_curves.map(x=>({name:'β='+x.beta,values:x.values}));format='0.00';break;}
case 'toy-training-loss':case 'toy-training-probability':{const d=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week07-workshop/workshop-report.json'),'utf8'));const rows=d.toy_history.filter(x=>x.step%10===0),probability=a.chart.endsWith('probability');type='line';categories=rows.map(x=>String(x.step));series=[{name:probability?'chosen 선택 확률':'DPO loss',values:rows.map(x=>probability?x.chosen_probability:x.loss)}];format=probability?'0.0%':'0.000';if(probability)max=1;break;}
case 'evaluation-fixtures':{const d=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week07-workshop/workshop-report.json'),'utf8'));const keys=['evidence','format','useful','no_excess_refusal'];categories=['근거','형식','유용성','과도한 거절 없음'];series=['baseline','candidate'].map(name=>({name,values:keys.map(k=>d.evaluation.rates[name][k])}));format='0.0%';max=1;majorUnit=.25;break;}
case 'sft-probability':{const data=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week06-concepts/concept-report.json'),'utf8'));categories=data.probability_loss.map(x=>String(x.probability));series=[{name:'정답 토큰 손실 (자연로그)',values:data.probability_loss.map(x=>x.loss)}];format='0.000';break;}
case 'uniform-quantization':{const data=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week06-concepts/concept-report.json'),'utf8'));categories=data.uniform_quantization.map(x=>x.bits+'-bit');series=[{name:'평균제곱오차',values:data.uniform_quantization.map(x=>x.mse)}];format='0.00000';break;}
case 'weight-storage':{const data=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/week06-concepts/concept-report.json'),'utf8'));categories=data.raw_weight_storage.map(x=>x.bits+'-bit');series=[{name:'가중치 원시 저장량 GB',values:data.raw_weight_storage.map(x=>x.raw_weight_gb)}];format='0.0';break;}
case 'adaptation-params':categories=['rank1','rank2','rank4','rank8'];series=[{name:'전체 행렬',values:[96,96,96,96]},{name:'두 행렬 합계',values:[20,40,80,160]}];format='0';break;
case 'adaptation-error':{const data=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/adaptation-labs/low-rank-report.json'),'utf8'));categories=data.metrics.map(x=>'rank'+x.rank);series=[{name:'상대 행렬 오차',values:data.metrics.map(x=>x.relative_error)}];format='0.000';max=1;break;}
case 'dpo-loss':type='line';categories=['-6','-3','0','3','6'];series=[{name:'DPO loss · beta=0.1',values:[-6,-3,0,3,6].map(m=>Math.log1p(Math.exp(-.1*m)))}];format='0.000';break;
case 'overlap':categories=['0','12','24','36'];series=[{name:'저장 문자 수',values:[94,106,118,166]}];format='0';break;
case 'threshold':categories=['0.10','0.25','0.50','0.90'];series=[{name:'원문 단어 겹침 비율',values:[1/6,1/6,1/6,1/6]}];format='0.0%';max=1;break;
case 'evaluation':categories=['BM25','BM25+확장','TF-IDF','RRF'];series=[{name:'Recall@3',values:chartData.map(x=>x.recall)},{name:'MRR@3',values:chartData.map(x=>x.mrr)}];format='0.0%';max=1;break;
case 'idf':type='line';categories=['1','2','4','6','8','10'];series=[{name:'IDF',values:[1,2,4,6,8,10].map(df=>Math.log(11/(df+1))+1)}];break;
case 'saturation':type='line';categories=['1','2','4','8','16'];series=[{name:'빈도 기여값',values:[1,2,4,8,16].map(f=>f*2.5/(f+1.5))}];break;
case 'length':type='line';categories=['50','100','200'];series=[{name:'b=0',values:[50,100,200].map(()=>5/3.5)},{name:'b=0.75',values:[50,100,200].map(dl=>5/(2+1.5*(.25+.75*dl/100)))}];max=2;majorUnit=.5;break;
case 'rrf':type='line';categories=['1','10','30','60'];series=[{name:'1위',values:[1,10,30,60].map(c=>1/(c+1))},{name:'5위',values:[1,10,30,60].map(c=>1/(c+5))}];format='0.000';break;
case 'k':categories=['k=1','k=3','k=5'];series=[{name:'Recall',values:[.833333333333,.833333333333,.833333333333]}];format='0.0%';max=1;break;
case 'timing':{const t=JSON.parse(await fs.readFile(path.join(ROOT,'output/validation/retrieval-timing.json'),'utf8'));categories=t.map((_,i)=>String(i+1));series=[{name:'검색 시간 ms',values:t}];type='line';break;}
default:throw Error('Unknown chart '+a.chart)}
// Six decimal places retain more precision than displayed, while making the
// embedded Excel snapshot losslessly representable. Raw measurements stay raw.
series=series.map(x=>({...x,values:x.values.map(v=>Math.round(v*1e6)/1e6)}));
const styles={typeface:FONT,fontSize:20,fill:C.gray};s.charts.add(type,{position:{left:70,top:190,width:1140,height:385},categories,series:series.map((x,i)=>({...x,valuesFormatCode:format,fill:[C.blue,C.navy,C.gray][i%3],line:{fill:[C.blue,C.navy,C.gray][i%3],width:2}})),hasLegend:series.length>1,legend:{position:'bottom',textStyle:styles},xAxis:{axisType:'textAxis',textStyle:styles},yAxis:{numberFormatCode:format,textStyle:styles,...(max?{min:0,max}:{}),...(majorUnit?{majorUnit}:{})},dataLabels:{showValue:type==='bar'&&series.length===1,textStyle:styles,numberFormatCode:format},lineOptions:{smooth:false},barOptions:{direction:'column',grouping:'clustered'},chartFill:'none',chartLine:{fill:'none',width:0},plotAreaFill:'none',plotAreaLine:{fill:'none',width:0}});note(s,a)}
async function imageLayout(s,a){
 shell(s,a);const file=path.join(ROOT,a.image),evaluation=week===5&&a.image.endsWith('lab-evaluation.jpg');
 let frame={left:64,top:168,width:evaluation?640:1152,height:380};
 if(a.imageMode==='side-explain')frame={left:80,top:171,width:550,height:410};
 if(a.imageMode==='wide-explain')frame={left:64,top:164,width:1152,height:300};
 if(a.imageMode==='tall-explain')frame={left:64,top:170,width:820,height:420};
 if(a.imageMode==='full-figure')frame={left:64,top:164,width:1152,height:410};
 s.images.add({blob:new Uint8Array(await fs.readFile(file)),contentType:a.image.endsWith('.jpg')?'image/jpeg':'image/png',alt:a.title,fit:'contain',position:frame});
 if(a.imageMode==='side-explain')a.items.forEach(([head,body],i)=>{const y=180+i*130;text(s,head,714,y,488,42,23,{bold:true});text(s,body,714,y+51,488,68,20,{color:C.gray});});
 else if(a.imageMode==='wide-explain')a.items.forEach(([head,body],i)=>{const x=64+i*390;text(s,head,x,481,366,36,21,{bold:true});text(s,body,x,530,366,62,18,{color:C.gray});});
 else if(a.imageMode==='tall-explain')a.items.forEach(([head,body],i)=>{const y=186+i*130;text(s,head,930,y,286,36,22,{bold:true});text(s,body,930,y+48,286,72,18,{color:C.gray});});
 else if(a.imageMode==='full-figure')a.items.forEach(([,body],i)=>text(s,body,64+i*390,583,366,38,18,{color:C.gray}));
 else {if(evaluation){text(s,'01 · 검색 지표',766,198,450,40,23,{bold:true});text(s,'정답 문서 회수율과\n첫 관련 문서의 순위',766,264,450,90,21,{color:C.gray});rule(s,766,374,450);text(s,'02 · 답변 보류',766,404,450,40,23,{bold:true});text(s,'답이 있는 질의와 없는 질의를\n분리해서 확인',766,468,450,82,21,{color:C.gray})}if(a.items.length)text(s,a.items.join(' · '),64,563,1152,42,17,{color:C.gray});}
 if(a.imageMode==='full-figure'&&a.caption)text(s,a.caption,64,632,1152,26,14,{color:C.gray});else note(s,a);
}
const renderers={cover,section,statement,focus,annotated,compare,steps,timeline:steps,flow,swimlane,table,case:caseLayout,code,formula,tokenmap,'lora-paths':loraPaths,'preference-pair':preferencePair,'dpo-paths':dpoPaths,windows,dates,rank,funnel,citation,ideas,roadmap,chart,notebook:caseLayout,links:caseLayout,image:imageLayout};
Object.assign(renderers,week09Renderers({shell,rect,rule,text,note,C}));
const auditWarnings=auditDeck(D,renderers);
for(const a of D.slides){current=a.n;const slide=p.slides.add();await renderers[resolveLayout(a)](slide,a);slide.speakerNotes.textFrame.setText(`${a.notes}\n\n[Sources]\n${a.sources.map(x=>'- '+x).join('\n')}\n[/Sources]`);slide.speakerNotes.setVisible(true)}
await fs.writeFile(path.join(BUILD,'geometry.json'),JSON.stringify(geometry));
const candidate=path.join(BUILD,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
if(D.slides.some(a=>a.monochrome))execFileSync(PY,[path.join(ROOT,'scripts/pptx_image_display.py'),candidate,...D.slides.filter(a=>a.monochrome).map(a=>String(a.n))]);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const finalDir=await fs.mkdtemp(path.join(BUILD,'final-'));
const finalPath=path.join(finalDir,D.name+'.pptx');
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,explicitTotalSlideCount:D.slides.length,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:[FONT,MONO]},verifyArtifactToolImport:true,materializeLiteralChartWorkbooks:true,receiptPath:path.join(BUILD,path.basename(finalDir)+'-validation.json')});
if(!noPublish){
 await fs.copyFile(finalPath,path.join(ROOT,`week${String(week).padStart(2,'0')}/lecture/${D.name}.pptx`));
 await fs.writeFile(path.join(ROOT,`week${String(week).padStart(2,'0')}/lecture/lecture-notes.md`),`# ${D.title}\n\n`+D.slides.map(a=>{
  const body=a.items.map(x=>Array.isArray(x)?x.join(' · '):x).join('\n\n');
  return `## ${a.n}. ${a.title}\n\n${body}${a.caption?`\n\n강의 포인트: ${a.caption}`:''}${a.notes?`\n\n${a.notes}`:''}\n\n근거: ${a.sources.join(', ')}`;
 }).join('\n\n'));
}
console.log(JSON.stringify({finalPath,published:!noPublish,slides:D.slides.length,minShapeFontPt:Math.min(...geometry.map(x=>x.pt)),layouts:[...new Set(D.slides.map(resolveLayout))],auditWarnings}));
