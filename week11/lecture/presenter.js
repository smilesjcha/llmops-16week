(() => {
 const $=s=>document.querySelector(s), protocol='llmops-week11-presenter-v1';
 const session=location.hash.slice(1), parent=window.opener;
 const origin=location.protocol==='file:'?'*':location.origin;
 let current=null,connected=false,ended=false,lastMessage=0,contentKey='',outlineKey='';
 function connection(ok,text){
  connected=ok;document.body.dataset.connected=String(ok);$('#connection').textContent=text;
  document.querySelectorAll('[data-control]').forEach(el=>el.disabled=!ok);
  if(ok&&current){$('#previous').disabled=current.page===1;$('#next').disabled=current.page===current.count;$('#flow-back').disabled=!current.flow||current.flow.backDisabled;}
 }
 function send(type,extra={}){
  if(!parent||parent.closed||ended)return;
  parent.postMessage({protocol,session,type,...extra},origin);
 }
 function command(action,extra={}){if(connected){send('hello');send('command',{action,...extra});}}
 function render(state){
  if(!Number.isInteger(state?.page)||!Number.isInteger(state.count)||state.page<1||state.page>state.count||typeof state.notes!=='string'||!Array.isArray(state.outline))return;
  current=state;lastMessage=Date.now();connection(true,'강의 창과 동기화 중');
  $('#waiting').hidden=true;$('#workspace').hidden=false;
  $('#position').textContent=state.page+' / '+state.count;$('#footer-position').textContent=state.page+' / '+state.count;
  $('#chapter').textContent=state.chapter;$('#slide-title').textContent=state.title;
  $('#next-title').textContent=state.page<state.count?(state.page+1)+'. '+state.nextTitle:state.nextTitle;
  document.title=state.page+'쪽 · 교수용 발표자 노트';
  $('#full-note').href='instructor/index.html#page-'+state.page;
  // Heartbeats must not reset a lecturer's reading position or unfinished input.
  const nextKey=state.page+'\n'+state.notes;
  if(nextKey!==contentKey){
   contentKey=nextKey;const root=$('#notes');root.replaceChildren();
   for(const block of state.notes.split('\n\n')){
    const [title,...lines]=block.split('\n'),section=document.createElement('section'),h=document.createElement('h2'),p=document.createElement('p');
    h.textContent=title;p.textContent=lines.join('\n');section.append(h,p);root.append(section);
   }
   $('#jump').value=state.page;$('#jump').max=state.count;window.scrollTo({top:0,behavior:'instant'});
  }
  const nextOutline=JSON.stringify(state.outline);
  if(nextOutline!==outlineKey){
   outlineKey=nextOutline;$('#outline').replaceChildren();
   for(const item of state.outline){const option=document.createElement('option');option.value=item.page;option.textContent=String(item.page).padStart(2,'0')+' · '+item.title;$('#outline').append(option);}
  }
  if(document.activeElement!==$('#outline'))$('#outline').value=String(state.page);
  $('#flow').hidden=!state.flow;if(state.flow)$('#flow-caption').textContent=state.flow.caption;
 }
 addEventListener('message',event=>{
  const data=event.data;
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
  if(event.metaKey||event.ctrlKey||event.altKey||!connected||/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
  const action=({ArrowRight:'next',PageDown:'next',ArrowLeft:'previous',PageUp:'previous',f:'flow-next',F:'flow-next'})[event.key];
  if(action){event.preventDefault();command(action);}
 });
 addEventListener('focus',heartbeat);addEventListener('pageshow',heartbeat);
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)heartbeat();});
 heartbeat();setInterval(heartbeat,1500);
})();
