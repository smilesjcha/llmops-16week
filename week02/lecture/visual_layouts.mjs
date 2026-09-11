/** Editable teaching diagrams and measured-data charts for Week 02.
 * Layout content comes from slide_content.json; no decorative raster drawing.
 */
import {createHash} from 'node:crypto';

export function renderTeachingVisual(s, spec, h) {
  const {txt,rect,rule,C,FONT,registerTable}=h, v=spec.visual;
  if(!v)return false;
  const t=(a,x,y,w,hh,pt=20,o={})=>txt(s,a,x,y,w,hh,pt,o);
  const note=a=>a&&t(a,64,607,1152,29,14,{color:C.gray});
  const line=(x,y,w,color=C.line)=>rule(s,x,y,w,color,2);
  const node=(label,x,y,w,hh,detail='',accent=false)=>{
    const shape=rect(s,x,y,w,hh,accent?C.soft:C.white,accent?C.blue:C.line,1);
    t(label,x+20,y+18,w-40,detail?40:hh-32,21,{bold:true,color:accent?C.blue:C.ink});
    if(detail)t(detail,x+20,y+63,w-40,hh-73,17,{color:C.gray});
    return shape;
  };
  // DrawingML tail is the destination end; head would point back to the source.
  const link=(a,b,from='right',to='left',color=C.gray)=>s.shapes.connect(a,b,{kind:from==='bottom'?'straight':'elbow',fromSide:from,toSide:to,line:{style:'solid',fill:color,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});

  switch(spec.layout){
    case 'service': {
      t('문의 T03',64,181,220,28,14,{color:C.gray});
      t(v.input,64,218,1152,99,27,{bold:true});
      const a=node('PROMPT/02',64,374,276,125,'분류와 답변 초안');
      const b=rect(s,430,349,410,201,C.white,C.line,1);
      v.outputs.forEach((r,i)=>{t(r.label,450,365+i*53,360,25,14,{color:C.gray});t(r.value,450,390+i*53,360,29,17,{bold:true});});
      const c=rect(s,932,369,284,158,C.white,C.line,1);
      t(v.reviewer,952,390,244,118,19,{bold:true});link(a,b);link(b,c);
      note(v.prohibited);break;
    }
    case 'pipeline': {
      const n=v.stages.length,w=(1152-44*(n-1))/n;
      const nodes=v.stages.map((st,i)=>{const x=64+i*(w+44);t(String(i+1).padStart(2,'0'),x,225,w,62,32,{color:C.gray});return node(st.label,x,316,w,160,st.detail);});
      nodes.slice(1).forEach((b,i)=>link(nodes[i],b));
      line(64,536,1152);t(v.failure,64,566,1152,38,20);break;
    }
    case 'anatomy': {
      const top=184,gap=88;
      v.blocks.forEach((b,i)=>{const y=top+i*gap;rect(s,260,y,956,70,i===3?C.soft:C.white);t(b.label,282,y+14,394,41,21,{bold:true});t(b.text,690,y+17,504,38,19,{color:C.gray});});
      t('system',64,220,178,40,23,{mono:true});t('고정 메시지',64,268,180,38,18,{color:C.gray});
      t('user',64,460,178,40,23,{mono:true,color:C.blue});t('문의 데이터',64,508,180,38,18,{color:C.gray});
      note(v.note);break;
    }
    case 'boundary': {
      t('SYSTEM / 업무 규칙',64,184,1152,30,16,{color:C.gray});
      t(v.rule,64,227,1152,55,28,{bold:true});
      s.shapes.add({geometry:'line',position:{left:64,top:318,width:1152,height:0},fill:'none',line:{fill:C.gray,width:2,style:'dashed'}});
      t('USER / 고객 원문',64,349,350,31,16,{color:C.gray});
      t(v.input,64,400,525,50,27);
      t(v.injection,664,395,552,106,23,{color:C.blue,bold:true});
      t('예상 처리',64,533,190,30,16,{color:C.gray});t(v.output,276,525,940,72,20,{mono:true});
      break;
    }
    case 'decision': {
      const q1=node(v.question,64,188,478,79);const q2=node(v.yesQuestion,64,367,478,79);
      const r1=node(v.branches[0].label,716,181,500,133,v.branches[0].result);
      const r2=node(v.branches[1].label,716,353,500,133,v.branches[1].result);
      const r3=rect(s,64,522,1152,68,C.white,C.line,1);t(v.branches[2].label,86,540,236,35,20,{bold:true});t(v.branches[2].result.replaceAll('\n',' '),365,539,829,39,20);
      link(q1,r1);link(q2,r2);link(q1,q2,'bottom','top');link(q2,r3,'bottom','top');
      t('아니오',572,192,112,28,14,{color:C.gray});t('아니오',572,366,112,28,14,{color:C.gray});t('예',325,303,76,29,14,{color:C.gray});t('예',326,471,76,29,14,{color:C.gray});break;
    }
    case 'syntax': {
      const values=[v.wrong,v.right],labels=['작은따옴표','큰따옴표'];
      values.forEach((code,i)=>{const x=64+i*608;t(labels[i],x,259,544,44,23,{bold:true});t(code,x,341,544,64,24,{mono:true,noWrap:true});[...code].forEach((c,k)=>{if(c==='\''||c==='"')line(x+k*24*4/3*0.61+3,397,13,i===1?C.blue:C.gray);});t(i?'JSON 파싱 통과':'JSON 파싱 실패',x,467,544,46,25,{bold:true});});
      note(v.note);break;
    }
    case 'gates': {
      const w=344;const nodes=v.stages.map((st,i)=>{const x=64+i*404;t(String(i+1).padStart(2,'0'),x,209,w,56,30,{color:C.gray});t(st.label,x,280,w,45,25,{bold:true});const n=rect(s,x,357,w,110,C.white,C.line,1);t(st.example,x+18,382,w-36,68,17,{mono:true});t(st.result,x,497,w,75,18);return n;});
      link(nodes[0],nodes[1]);link(nodes[1],nodes[2]);note(v.note);break;
    }
    case 'outcome': {
      t(v.input,64,196,1152,85,28,{bold:true});line(64,303,1152);
      t('실제 응답 · T03 / v2',64,339,520,33,16,{color:C.gray});t('업무 기준',704,339,512,33,16,{color:C.gray});
      t(v.actual,64,390,550,74,34,{bold:true,color:C.blue});t(v.expected,704,390,512,74,34,{bold:true});
      t(`응답 초안: ${v.reply}`,64,491,1152,45,18,{color:C.gray});
      t(`배포 시 예상 영향   ${v.impact}`,64,566,1152,40,22);break;
    }
    case 'intent': {
      v.clauses.forEach((c,i)=>{const x=64+i*608;t(c.text,x,230,544,124,31,{bold:true});line(x,372,544,i?C.blue:C.gray);t(c.label,x,407,544,61,23,{color:i?C.blue:C.gray});});
      t(v.question,64,555,1152,65,24,{bold:true});break;
    }
    case 'versions': {
      const nodes=v.nodes.map((n,i)=>{const x=64+i*404;t(n.version,x,202,344,70,40,{mono:true,bold:true});return node(n.change,x,305,344,110);});
      link(nodes[0],nodes[1]);link(nodes[1],nodes[2]);const branch=rect(s,458,478,410,98,C.white,C.line,1);t(v.branch,478,496,370,66,20);link(nodes[1],branch,'bottom','top');note(v.note);break;
    }
    case 'hashdiff': {
      const values=[v.leftContent,v.rightContent];
      values.forEach((a,i)=>{const y=213+i*187;t('v2.md',64,y,170,37,20,{mono:true});t(a,264,y,952,48,24,{bold:true});const digest=createHash('sha256').update(a,'utf8').digest('hex');t('SHA-256',264,y+77,210,32,16,{color:C.gray,mono:true});t(digest.slice(0,16),514,y+69,702,48,25,{mono:true,color:i?C.blue:C.ink});if(i===0)line(64,y+147,1152);});note(`${v.note} · 표시값은 UTF-8 원문의 해시 앞 16자리`);break;
    }
    case 'experiment': {
      const input=node(v.input,64,317,285,109);const checks=node('같은 검사 기준',878,287,338,169,v.checks.join(' / '));
      const versions=v.versions.map((vv,i)=>node(vv,501,184+i*143,235,84,'',true));
      versions.forEach(n=>{link(input,n);link(n,checks);});
      t('고정 조건',64,585,178,37,18,{bold:true});t(v.fixed.join(' / '),274,583,942,62,18,{color:C.gray});break;
    }
    case 'matrix': {
      const headers=['문의 / 버전',...v.headers];const rows=[headers,...v.rows.map(r=>[r.label,...r.values.map(x=>x==='pass'?'통과':x==='fail'?'실패':'미평가')])];
      const widths=[312,210,210,210,210];
      const table=s.tables.add({rows:rows.length,columns:5,left:64,top:224,width:1152,height:222,columnWidths:widths,values:rows});table.styleOptions={headerRow:false,bandedRows:false};table.borders.assign({fill:C.line,width:1,style:'solid'});
      rows.forEach((row,r)=>{table.rows[r].height=74;row.forEach((value,c)=>{const cell=table.getCell(r,c),fail=value==='실패';cell.fill=r===0?C.ink:fail?C.soft:C.white;cell.text.style={typeface:FONT,fontSize:(r===0?18:21)*4/3,color:r===0?C.white:fail?C.blue:C.ink,bold:r===0||fail,autoFit:'none',wrap:'none',verticalAlignment:'middle',alignment:c?'center':'left',insets:{left:18,right:18,top:14,bottom:14}};});});registerTable(spec.n);
      v.definitions.forEach((a,i)=>{const x=64+i*295;t(v.headers[i],x,491,264,32,17,{bold:true});t(a,x,539,264,60,17,{color:C.gray});});note('형식이 실패하면 뒤의 업무 검사는 미평가 · 전체 통과는 네 항목 모두 충족');break;
    }
    case 'recovery': {
      const ns=v.checks.map((c,i)=>{const y=188+i*101;const n=node(c.question,64,y,546,75);t('아니오',631,y-8,100,29,14,{color:C.gray});const out=rect(s,759,y,457,75,'none');t(c.fix,779,y+20,417,47,18);link(n,out);return n;});
      ns.slice(1).forEach((n,i)=>link(ns[i],n,'bottom','top'));note(v.note);break;
    }
    case 'cadence': {
      t('격주 출제 · 매 과제 일주일',64,187,1152,50,25,{bold:true});
      [v.releaseWeek,v.dueWeek].forEach((a,i)=>{const x=64+i*720;t(a,x,287,432,35,18,{color:C.gray});t(i?v.dueDate:v.releaseDate,x,350,432,95,50,{bold:true,mono:true});});
      line(64,476,1152,C.ink);rect(s,64,470,14,14,C.ink);rect(s,1202,470,14,14,C.ink);
      t(v.rule,64,513,1152,63,23);note(v.exception);break;
    }
    case 'deliverables': {
      v.files.forEach((f,i)=>{const x=64+i*608;t(f.name,x,212,544,100,29,{bold:true});line(x,324,544);t(f.description,x,354,544,94,21,{color:C.gray});});
      t('보고서의 원문·해시',64,505,470,40,22,{bold:true});t('분석 문서의 사례 근거',704,505,512,40,22,{bold:true});
      const a=rect(s,545,515,1,1,'none'),b=rect(s,672,515,1,1,'none');link(a,b);
      t(v.questions.join(' / '),64,575,1152,61,16,{color:C.gray});break;
    }
    case 'submission': {
      const common=node('동일한 과제',64,299,345,135,'JSON 보고서 + 분석 PDF');
      const routes=v.routes.map((r,i)=>{const y=191+i*187;const shape=rect(s,650,y,566,149,C.white,C.line,1);t(r.audience,674,y+20,518,37,20,{bold:true});t(r.destination,674,y+79,518,53,24);return shape;});
      routes.forEach(n=>link(common,n));t(v.deadline,64,551,1152,49,26,{bold:true});note(v.note);break;
    }
    default:return false;
  }
  return true;
}
