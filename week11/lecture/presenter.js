(() => {
 const $=s=>document.querySelector(s),protocol='llmops-week11-presenter-v1',previewProtocol='llmops-week11-preview-v1';
 const session=location.hash.slice(1),parent=window.opener,origin=location.protocol==='file:'?'*':location.origin;
 let current=null,connected=false,ended=false,lastMessage=0,contentKey='',outlineKey='',havePreviews=false,expandedKind=null;
 const frames=new Map(['current','next','expanded'].map(slot=>[slot,{slot,frame:$('#'+slot+'-preview'),stage:$('#'+slot+'-stage'),ready:false,loaded:false,slide:null,revision:0}]));
 const FONT_KEY='llmops.week11.presenter.noteFontSize',FONT_DEFAULT=22,FONT_MIN=16,FONT_MAX=36;
 let fontSize=FONT_DEFAULT;
 try{const stored=Number(localStorage.getItem(FONT_KEY));if(Number.isFinite(stored)&&stored>=FONT_MIN&&stored<=FONT_MAX)fontSize=stored;}catch{}
 function setFont(value,persist=true){
  const notes=$('#notes'),range=notes.scrollHeight-notes.clientHeight,progress=range>0?notes.scrollTop/range:0;
  fontSize=Math.max(FONT_MIN,Math.min(FONT_MAX,Math.round(value)));
  document.documentElement.style.setProperty('--note-size',fontSize+'px');
  $('#font-size').value=String(fontSize);$('#font-size').setAttribute('aria-valuetext',fontSize+'픽셀');$('#font-value').textContent=fontSize+'px';
  $('#font-smaller').disabled=fontSize===FONT_MIN;$('#font-larger').disabled=fontSize===FONT_MAX;
  if(persist)try{localStorage.setItem(FONT_KEY,String(fontSize));}catch{}
  notes.scrollTop=progress*Math.max(0,notes.scrollHeight-notes.clientHeight);
 }
 $('#font-size').oninput=()=>setFont(Number($('#font-size').value));$('#font-smaller').onclick=()=>setFont(fontSize-2);$('#font-larger').onclick=()=>setFont(fontSize+2);$('#font-reset').onclick=()=>setFont(FONT_DEFAULT);
 setFont(fontSize,false);
 function fitFrame(entry){
  const width=entry.stage.clientWidth,height=entry.stage.clientHeight;
  if(width&&height)entry.stage.style.setProperty('--preview-scale',Math.min(width/1440,height/810));
 }
 function fitNotes(){
  const notes=$('#notes');
  if(innerWidth<=760){notes.style.height='';$('#visual-pane').style.maxHeight='';$('#pane-divider').style.height='';return;}
  const panelHeight=Math.max(200,innerHeight-$('#visual-pane').getBoundingClientRect().top-$('footer.controls').offsetHeight-20);
  $('#visual-pane').style.maxHeight=panelHeight+'px';$('#pane-divider').style.height=panelHeight+'px';
  const available=innerHeight-notes.getBoundingClientRect().top-$('footer.controls').offsetHeight-$('.notes-pane .help').offsetHeight-($('#flow').hidden?0:$('#flow').offsetHeight+32)-28;
  notes.style.height=Math.max(200,available)+'px';
 }
 const SPLIT_KEY='llmops.week11.presenter.previewShare',SPLIT_DEFAULT=47.5;
 const layout=$('.layout'),divider=$('#pane-divider');
 let preferredShare=SPLIT_DEFAULT,effectiveShare=SPLIT_DEFAULT,drag=null,layoutFrame=0;
 try{const saved=Number(localStorage.getItem(SPLIT_KEY));if(Number.isFinite(saved)&&saved>=20&&saved<=75)preferredShare=saved;}catch{}
 function splitBounds(){
  const width=layout.clientWidth-divider.offsetWidth;
  // Keep both previews and large-text notes usable, even on a narrow laptop window.
  return {width,min:Math.max(20,Math.ceil(280/width*100)),max:Math.min(75,Math.floor((width-340)/width*100))};
 }
 function applySplit(){
  if($('#workspace').hidden)return;
  const notes=$('#notes'),range=notes.scrollHeight-notes.clientHeight,progress=range>0?notes.scrollTop/range:0;
  if(innerWidth>760){
   const bounds=splitBounds();
   effectiveShare=Math.max(bounds.min,Math.min(bounds.max,preferredShare));
   layout.style.setProperty('--preview-fr',effectiveShare+'fr');layout.style.setProperty('--notes-fr',(100-effectiveShare)+'fr');
   divider.setAttribute('aria-valuemin',bounds.min);divider.setAttribute('aria-valuemax',bounds.max);divider.setAttribute('aria-valuenow',effectiveShare);
   divider.setAttribute('aria-valuetext',`장표 ${effectiveShare}%, 노트 ${Number((100-effectiveShare).toFixed(1))}%`);
   $('#split-value').textContent=`장표 ${Math.round(effectiveShare)}% · 노트 ${100-Math.round(effectiveShare)}%`;
  }
  fitNotes();notes.scrollTop=progress*Math.max(0,notes.scrollHeight-notes.clientHeight);
 }
 function saveSplit(){try{localStorage.setItem(SPLIT_KEY,String(preferredShare));}catch{}}
 function setSplit(value,persist=true){
  const {min,max}=splitBounds();preferredShare=Math.max(min,Math.min(max,Math.round(value*10)/10));
  applySplit();if(persist)saveSplit();
 }
 function resetSplit(){preferredShare=SPLIT_DEFAULT;applySplit();saveSplit();}
 function finishDrag(event){
  if(!drag||(event?.pointerId!==undefined&&event.pointerId!==drag.id))return;
  const id=drag.id;drag=null;document.body.classList.remove('resizing-panes');
  if(divider.hasPointerCapture(id))divider.releasePointerCapture(id);
  saveSplit();
 }
 divider.addEventListener('pointerdown',event=>{
  if(!event.isPrimary||event.button!==0||innerWidth<=760)return;
  event.preventDefault();divider.focus({preventScroll:true});
  drag={id:event.pointerId,x:event.clientX,share:effectiveShare};divider.setPointerCapture(event.pointerId);
  document.body.classList.add('resizing-panes');
 });
 divider.addEventListener('pointermove',event=>{
  if(!drag||event.pointerId!==drag.id)return;
  setSplit(drag.share+(event.clientX-drag.x)/splitBounds().width*100,false);
 });
 for(const event of ['pointerup','pointercancel','lostpointercapture'])divider.addEventListener(event,finishDrag);
 addEventListener('blur',()=>finishDrag());
 divider.addEventListener('keydown',event=>{
  if(event.altKey||event.ctrlKey||event.metaKey)return;
  const step=event.shiftKey?10:2,{min,max}=splitBounds();
  const value={ArrowLeft:effectiveShare-step,ArrowRight:effectiveShare+step,Home:min,End:max}[event.key];
  // Divider arrows resize the panes instead of advancing the audience's slide.
  if(value!==undefined||event.key==='Enter'){event.preventDefault();event.stopPropagation();event.key==='Enter'?resetSplit():setSplit(value);}
 });
 divider.addEventListener('dblclick',resetSplit);$('#split-reset').onclick=resetSplit;
 function scheduleLayout(){cancelAnimationFrame(layoutFrame);layoutFrame=requestAnimationFrame(applySplit);}
 addEventListener('resize',()=>{finishDrag();scheduleLayout();});
 const panelResize=new ResizeObserver(scheduleLayout);
 for(const node of [$('.notes-toolbar'),$('.notes-pane .help'),$('#flow')])panelResize.observe(node);
 const resize=new ResizeObserver(entries=>{for(const item of entries)for(const entry of frames.values())if(entry.stage===item.target)fitFrame(entry);});
 for(const entry of frames.values())resize.observe(entry.stage);
 function loadFrame(entry){
  if(entry.loaded)return;entry.loaded=true;
  const url=new URL('preview.html',location.href);url.hash=session+'~'+entry.slot;entry.frame.src=url.href;
 }
 function sendPreview(entry){
  if(!entry.ready||!entry.slide)return;
  // The read-only iframe has an opaque sandbox origin; source + session bind replies.
  entry.frame.contentWindow.postMessage({protocol:previewProtocol,session,slot:entry.slot,type:'render',revision:entry.revision,slide:entry.slide},'*');
 }
 function queuePreview(slot,slide){
  const entry=frames.get(slot);
  if(!slide){entry.slide=null;entry.stage.hidden=true;return;}
  entry.stage.hidden=false;
  if(entry.slide?.page===slide.page&&entry.slide?.html===slide.html)return;
  entry.slide=slide;entry.revision++;entry.stage.setAttribute('aria-busy','true');entry.stage.removeAttribute('data-page');
  loadFrame(entry);sendPreview(entry);fitFrame(entry);
 }
 function updatePreviews(previews){
  havePreviews=true;
  queuePreview('current',previews.current);queuePreview('next',previews.next);
  $('#current-preview-label').textContent='현재 · '+previews.current.page+'쪽';
  $('#next-preview-label').textContent=previews.next?'다음 · '+previews.next.page+'쪽':'다음 장표 없음';
  $('#preview-end').hidden=Boolean(previews.next);$('#expand-current').disabled=false;$('#expand-next').disabled=!previews.next;
  if(expandedKind){
   const slide=previews[expandedKind];
   if(slide){queuePreview('expanded',slide);$('#preview-dialog-title').textContent=(expandedKind==='current'?'현재':'다음')+' · '+slide.page+'쪽 · '+slide.title;}
   else $('#preview-dialog').close();
  }
 }
 function openExpanded(kind){
  const slide=frames.get(kind).slide;if(!slide)return;
  expandedKind=kind;$('#preview-dialog-title').textContent=(kind==='current'?'현재':'다음')+' · '+slide.page+'쪽 · '+slide.title;
  $('#preview-dialog').showModal();queuePreview('expanded',slide);fitFrame(frames.get('expanded'));
 }
 $('#expand-current').onclick=()=>openExpanded('current');$('#expand-next').onclick=()=>openExpanded('next');
 $('#preview-close').onclick=()=>$('#preview-dialog').close();$('#preview-dialog').addEventListener('close',()=>expandedKind=null);
 function connection(ok,text){
  connected=ok;document.body.dataset.connected=String(ok);$('#connection').textContent=text;
  document.querySelectorAll('[data-control]').forEach(el=>el.disabled=!ok);
  if(ok&&current){$('#previous').disabled=current.page===1;$('#next').disabled=current.page===current.count;$('#flow-back').disabled=!current.flow||current.flow.backDisabled;}
 }
 function send(type,extra={}){
  if(!parent||parent.closed||ended)return;
  parent.postMessage({protocol,session,type,...(type==='hello'?{wantPreviews:!havePreviews}:{}),...extra},origin);
 }
 function command(action,extra={}){if(connected){send('hello');send('command',{action,...extra});}}
 function render(state){
  if(!Number.isInteger(state?.page)||!Number.isInteger(state.count)||state.page<1||state.page>state.count||typeof state.notes!=='string'||!Array.isArray(state.outline))return;
  const changedPage=current?.page!==state.page;
  current=state;lastMessage=Date.now();connection(true,'강의 창과 동기화 중');
  const firstRender=$('#workspace').hidden;
  $('#waiting').hidden=true;$('#workspace').hidden=false;
  $('#position').textContent=state.page+' / '+state.count;$('#footer-position').textContent=state.page+' / '+state.count;
  $('#chapter').textContent=state.chapter;$('#slide-title').textContent=state.title;
  $('#next-title').textContent=state.page<state.count?state.nextTitle:'강의 마무리';
  document.title=state.page+'쪽 · 교수용 발표자 노트';$('#full-note').href='instructor/index.html#page-'+state.page;
  // Heartbeats do not reset the lecturer's notes, preview documents or unfinished input.
  const nextKey=state.page+'\n'+state.notes;
  if(nextKey!==contentKey){
   contentKey=nextKey;const root=$('#notes');root.replaceChildren();
   for(const block of state.notes.split('\n\n')){
    const [title,...lines]=block.split('\n'),section=document.createElement('section'),h=document.createElement('h2'),p=document.createElement('p');
    h.textContent=title;p.textContent=lines.join('\n');section.append(h,p);root.append(section);
   }
   $('#jump').value=state.page;$('#jump').max=state.count;root.scrollTop=0;$('#visual-pane').scrollTop=0;window.scrollTo({top:0,behavior:'instant'});
  }
  const nextOutline=JSON.stringify(state.outline);
  if(nextOutline!==outlineKey){
   outlineKey=nextOutline;$('#outline').replaceChildren();
   for(const item of state.outline){const option=document.createElement('option');option.value=item.page;option.textContent=String(item.page).padStart(2,'0')+' · '+item.title;$('#outline').append(option);}
  }
  if(document.activeElement!==$('#outline'))$('#outline').value=String(state.page);
  $('#flow').hidden=!state.flow;if(state.flow)$('#flow-caption').textContent=state.flow.caption;
  if(firstRender)applySplit();else fitNotes();
  if(state.previews?.current?.page===state.page&&typeof state.previews.current.html==='string'&&(state.previews.next===null||state.previews.next?.page===state.page+1))updatePreviews(state.previews);
  else if(changedPage){havePreviews=false;for(const slot of ['current','next'])frames.get(slot).stage.setAttribute('aria-busy','true');}
 }
 addEventListener('message',event=>{
  const data=event.data;
  if(data?.protocol===previewProtocol){
   const entry=frames.get(data.slot);
   if(!entry||event.source!==entry.frame.contentWindow||event.origin!=='null'||data.session!==session)return;
   if(data.type==='ready'){entry.ready=true;sendPreview(entry);}
   else if(data.type==='rendered'&&data.revision===entry.revision&&data.page===entry.slide?.page){entry.stage.setAttribute('aria-busy','false');entry.stage.dataset.page=String(data.page);}
   return;
  }
  if(ended||event.source!==parent||event.origin!==(location.protocol==='file:'?'null':location.origin)||!data||data.protocol!==protocol||data.session!==session)return;
  if(data.type==='state')render(data.state);
  else if(data.type==='paused')connection(false,'강의 창 연결을 다시 확인하는 중');
  else if(data.type==='ended'){ended=true;connection(false,'발표자 모드 종료 · 다시 시작하려면 강의 창의 버튼을 누르세요.');}
 });
 function heartbeat(){
  if(ended)return;
  if(!parent||parent.closed){connection(false,'강의 창 연결 없음 · 강의안의 발표자 모드로 다시 시작하세요.');return;}
  if(lastMessage&&Date.now()-lastMessage>10000)connection(false,'동기화 대기 · 마지막으로 받은 노트입니다. 강의 창을 확인하세요.');
  send('hello');
 }
 $('#previous').onclick=()=>command('previous');$('#next').onclick=()=>command('next');
 $('#jump-form').onsubmit=event=>{event.preventDefault();const page=Number($('#jump').value);if(Number.isInteger(page)&&page>=1&&page<=current?.count)command('goto',{page});};
 $('#outline').onchange=()=>command('goto',{page:Number($('#outline').value)});
 for(const action of ['flow-next','flow-back','flow-reset'])$('#'+action).onclick=()=>command(action);
 $('#audience-focus').onclick=()=>{if(connected)parent.focus();};$('#end').onclick=()=>command('end');
 addEventListener('keydown',event=>{
  if(event.metaKey||event.ctrlKey||event.altKey||!connected||$('#preview-dialog').open||/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
  const action=({ArrowRight:'next',PageDown:'next',ArrowLeft:'previous',PageUp:'previous',f:'flow-next',F:'flow-next'})[event.key];
  if(action){event.preventDefault();command(action);}
 });
 addEventListener('focus',heartbeat);addEventListener('pageshow',heartbeat);
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)heartbeat();});
 heartbeat();setInterval(heartbeat,1500);
})();
