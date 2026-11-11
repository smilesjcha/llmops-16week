(() => {
 const slides=[...document.querySelectorAll('.slide')], $=s=>document.querySelector(s);
 let current=0,previousFocus=null,presentationMode=false,uiTimer=null,noticeTimer=null;
 // A private window pair; ordinary student tabs do not subscribe to this session.
 const presenterProtocol='llmops-week11-presenter-v1';
 const restorePresenter=['reload','back_forward'].includes(performance.getEntriesByType('navigation')[0]?.type);
 const presenterSession=(restorePresenter&&history.state?.week11Session)||crypto.randomUUID();
 let presenterActive=restorePresenter&&history.state?.week11Presenter===true,presenterWindow=null,presenterFeedbackTimer=null;
 const messageOrigin=location.protocol==='file:'?'*':location.origin;
 const outline=slides.map((slide,index)=>({page:index+1,title:slide.getAttribute('aria-label').replace(/^\d+페이지 /,''),chapter:slide.dataset.chapter}));
 function rememberPresenter(url=location.href){history.replaceState({...history.state,week11Session:presenterSession,week11Presenter:presenterActive},'',url);}
 function applyPresenterMode(){
  document.documentElement.classList.toggle('audience-mode',presenterActive);
  $('#presenter-stop').hidden=!presenterActive;
  $('#presenter-button').textContent=presenterActive?'발표자 창':'발표자 모드';
  $('#presenter-button').setAttribute('aria-pressed',String(presenterActive));
  if(presenterActive){$('#notes-panel').classList.remove('open');$('#notes-panel').inert=true;$('#notes-button').setAttribute('aria-expanded','false');}
  rememberPresenter();
 }
 function previewSlide(index){
  const source=slides[index];if(!source)return null;
  const clone=source.cloneNode(true);clone.classList.add('active');
  clone.removeAttribute('aria-hidden');clone.removeAttribute('inert');
  clone.querySelector('.presenter-note')?.remove();clone.querySelectorAll('.enlarge').forEach(el=>el.remove());
  clone.querySelectorAll('input').forEach((el,i)=>{el.setAttribute('value',source.querySelectorAll('input')[i].value);});
  return {page:index+1,title:outline[index].title,html:clone.outerHTML};
 }
 function presenterState(includePreviews){
  const walk=slides[current].querySelector('.diagram-walk');
  return {page:current+1,count:slides.length,title:outline[current].title,chapter:outline[current].chapter,
   notes:slides[current].querySelector('.presenter-note').textContent,
   nextTitle:outline[current+1]?.title||'마지막 장표',outline,
   ...(includePreviews?{previews:{current:previewSlide(current),next:previewSlide(current+1)}}:{}),
   flow:walk?{caption:walk.querySelector('.walk-caption').textContent,backDisabled:walk.querySelector('.walk-back').disabled}:null};
 }
 function sendPresenter(type='state',includePreviews=true){
  if(!presenterActive||!presenterWindow||presenterWindow.closed)return;
  presenterWindow.postMessage({protocol:presenterProtocol,session:presenterSession,type,...(type==='state'?{state:presenterState(includePreviews)}:{})},messageOrigin);
 }
 function openPresenter(){
  presenterActive=true;applyPresenterMode();
  if(presenterWindow&&!presenterWindow.closed){presenterWindow.focus();sendPresenter();return;}
  const url=new URL('presenter.html',location.href);url.hash=presenterSession;
  presenterWindow=window.open(url.href,'week11-presenter-'+presenterSession,'popup=yes,width=1120,height=880,resizable=yes,scrollbars=yes');
  const hint=$('#presenter-feedback');
  hint.textContent=presenterWindow?'발표자 창에서 연결 상태를 확인하세요. 강의 창만 공유한 뒤 P로 전체화면을 시작합니다.':'팝업이 차단되었습니다. 이 사이트의 팝업을 허용한 뒤 발표자 창 버튼을 다시 누르세요.';
  hint.hidden=false;clearTimeout(presenterFeedbackTimer);presenterFeedbackTimer=setTimeout(()=>hint.hidden=true,10000);
  if(presenterWindow){presenterWindow.focus();sendPresenter();}
 }
 function endPresenter(){
  sendPresenter('ended');presenterWindow?.close();presenterActive=false;presenterWindow=null;applyPresenterMode();
  $('#presenter-feedback').hidden=true;setNotes(false);
 }
 addEventListener('message',event=>{
  const data=event.data;
  if(!presenterActive||!data||data.protocol!==presenterProtocol||data.session!==presenterSession)return;
  if(event.origin!==(location.protocol==='file:'?'null':location.origin))return;
  if(presenterWindow&&event.source!==presenterWindow)return;
  const reconnected=!presenterWindow;
  if(!presenterWindow){
   if(data.type!=='hello')return;
   // Recover the window reference after reloading this deck, without a broadcast.
   try{if(event.source?.opener!==window)return;}catch{return;}
   presenterWindow=event.source;
  }
  if(data.type==='hello'){sendPresenter('state',reconnected||data.wantPreviews===true);return;}
  if(data.type!=='command')return;
  if(presentationMode){document.activeElement?.blur();clearTimeout(uiTimer);document.documentElement.classList.remove('presentation-ui');}
  if(data.action==='next')show(current+1);
  else if(data.action==='previous')show(current-1);
  else if(data.action==='goto'&&Number.isInteger(data.page)&&data.page>=1&&data.page<=slides.length)show(data.page-1);
  else if(data.action==='flow-next')slides[current].querySelector('.walk-next')?.click();
  else if(data.action==='flow-back')slides[current].querySelector('.walk-back')?.click();
  else if(data.action==='flow-reset')slides[current].querySelector('.walk-reset')?.click();
  else if(data.action==='end')endPresenter();
 });
 addEventListener('pagehide',()=>sendPresenter('paused'));

 function scale(){
  const fit=presentationMode?Math.min(innerWidth/1440,innerHeight/810):Math.min(1,(innerWidth-32)/1440,(innerHeight-144)/810);
  document.documentElement.style.setProperty('--scale',String(fit));
 }
 function revealPresentationUI(){
  if(!presentationMode)return;
  document.documentElement.classList.add('presentation-ui');clearTimeout(uiTimer);
  uiTimer=setTimeout(()=>document.documentElement.classList.remove('presentation-ui'),2200);
 }
 function setPresentationMode(active){
  presentationMode=active;document.documentElement.classList.toggle('presentation-mode',active);
  $('#fullscreen').textContent=active?'전체화면 종료':'전체 화면';
  $('#fullscreen').setAttribute('aria-pressed',String(active));
  scale();window.scrollTo({top:0,behavior:'instant'});
  clearTimeout(uiTimer);clearTimeout(noticeTimer);
  document.documentElement.classList.remove('presentation-ui');$('#presentation-notice').textContent='';
  if(active){$('#presenter-feedback').hidden=true;document.activeElement?.blur();revealPresentationUI();}
 }
 async function toggleFullscreen(){
  if(document.fullscreenElement){await document.exitFullscreen();return;}
  if(presentationMode){setPresentationMode(false);return;}
  try{
   await document.documentElement.requestFullscreen({navigationUI:'hide'});
  }catch{
   setPresentationMode(true);
   $('#presentation-notice').textContent='브라우저 전체화면이 제한되어 창 안에서 발표합니다. Chrome·Edge의 새 탭에서 다시 시도하세요. P 또는 Esc로 종료.';
   noticeTimer=setTimeout(()=>$('#presentation-notice').textContent='',8000);
  }
 }
 addEventListener('fullscreenchange',()=>setPresentationMode(Boolean(document.fullscreenElement)));
 addEventListener('pointermove',e=>{if(e.clientY<48||e.clientY>innerHeight-88)revealPresentationUI();});
 addEventListener('pointerdown',e=>{if(e.pointerType==='touch')revealPresentationUI();});
 addEventListener('focusin',e=>{if(e.target.closest('.controls,#chapter-nav'))revealPresentationUI();});
 function show(n,update=true){
  if(!Number.isFinite(n))return;
  current=Math.max(0,Math.min(slides.length-1,Math.trunc(n)));
  slides.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',i===current?'false':'true');s.inert=i!==current;});
  $('#status').textContent=(current+1)+' / '+slides.length;$('#jump').value=current+1;
  $('#previous').disabled=current===0;$('#next').disabled=current===slides.length-1;
  const noteRoot=$('#notes-text');noteRoot.replaceChildren();
  $('#notes-title').textContent=String(current+1).padStart(2,'0')+' · '+slides[current].getAttribute('aria-label').replace(/^\d+페이지 /,'');
  $('#instructor-link').href='instructor/index.html#page-'+(current+1);
  for(const block of slides[current].querySelector('.presenter-note').textContent.split('\n\n')){
   const [label,...lines]=block.split('\n'),section=document.createElement('section');
   const heading=document.createElement('h3');heading.textContent=label;
   const paragraph=document.createElement('p');paragraph.textContent=lines.join('\n');
   section.append(heading,paragraph);noteRoot.append(section);
  }
  $('#notes-panel').scrollTop=0;
  document.querySelectorAll('#chapter-nav button').forEach(b=>{if(b.dataset.chapter===slides[current].dataset.chapter)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
  rememberPresenter(update?'#slide-'+(current+1):location.href);
  if(!presentationMode&&matchMedia('(max-width:1100px), (max-height:640px)').matches)window.scrollTo({top:0,behavior:'instant'});
  sendPresenter();
 }
 function fromHash(){const n=Number(location.hash.replace('#slide-',''));return Number.isFinite(n)&&n>0?n-1:0;}
 document.documentElement.classList.add('js');
 $('#previous').onclick=()=>show(current-1);$('#next').onclick=()=>show(current+1);
 $('#jump').onchange=()=>show(Number($('#jump').value)-1);
 function closeOverview(){$('#overview').classList.remove('open');$('#overview').inert=true;previousFocus?.focus();}
 $('#overview-button').onclick=()=>{previousFocus=document.activeElement;$('#overview').inert=false;$('#overview').classList.add('open');$('#overview-search').focus();};
 $('#overview-close').onclick=closeOverview;
 const chapters=new Map();
 slides.forEach((s,i)=>{const title=s.dataset.chapter||'강의';if(!chapters.has(title))chapters.set(title,[]);chapters.get(title).push({slide:s,index:i});});
 for(const [title,items] of chapters){
  const navButton=document.createElement('button');navButton.dataset.chapter=title;navButton.textContent=title.replace(/^\d+ /,'');navButton.onclick=()=>show(items[0].index);$('#chapter-nav').append(navButton);
  const section=document.createElement('section');section.className='overview-chapter';
  const heading=document.createElement('h3');heading.textContent=title;section.append(heading);
  const group=document.createElement('div');group.className='chapter-items';
  for(const {slide,index} of items){const button=document.createElement('button');button.dataset.slide=index;button.textContent=String(index+1).padStart(2,'0')+'　'+slide.querySelector('h1,h2').textContent;group.append(button);}
  section.append(group);$('.overview-list').append(section);
 }
 $('#overview-search').oninput=()=>{const query=$('#overview-search').value.trim().toLocaleLowerCase();let count=0;for(const group of document.querySelectorAll('.overview-chapter')){let shown=0;for(const b of group.querySelectorAll('[data-slide]')){const match=b.textContent.toLocaleLowerCase().includes(query)||group.querySelector('h3').textContent.toLocaleLowerCase().includes(query);b.hidden=!match;if(match){shown++;count++;}}group.hidden=shown===0;}$('#overview-empty').hidden=count>0;};
 $('.overview-list').onclick=e=>{const b=e.target.closest('[data-slide]');if(b){show(Number(b.dataset.slide));closeOverview();}};
 function setNotes(opened){if(opened&&presenterActive){openPresenter();return;}$('#notes-panel').classList.toggle('open',opened);$('#notes-panel').inert=!opened;$('#notes-button').setAttribute('aria-expanded',String(opened));}
 $('#notes-panel').inert=true;
 $('#notes-button').onclick=()=>setNotes(!$('#notes-panel').classList.contains('open'));
 $('#notes-close').onclick=()=>{setNotes(false);$('#notes-button').focus();};
 $('#presenter-button').onclick=openPresenter;
 $('#presenter-stop').onclick=endPresenter;
 applyPresenterMode();
 $('#fullscreen').onclick=toggleFullscreen;
 $('#print').onclick=()=>window.print();
 addEventListener('keydown',e=>{
  if($('#image-viewer').open)return;
  if(e.metaKey||e.ctrlKey||e.altKey)return;
  if($('#overview').classList.contains('open')){
   if(e.key==='Escape'){closeOverview();e.preventDefault();}
   if(e.key==='Tab'){const items=[...$('#overview').querySelectorAll('button,input')].filter(el=>!el.hidden&&!el.closest('[hidden]')),first=items[0],last=items.at(-1);if(e.shiftKey&&document.activeElement===first){last.focus();e.preventDefault();}else if(!e.shiftKey&&document.activeElement===last){first.focus();e.preventDefault();}}
   return;
  }
  if(e.key==='Escape'&&presentationMode&&!document.fullscreenElement){setPresentationMode(false);e.preventDefault();return;}
  if(/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
  if(e.key.toLowerCase()==='p'){toggleFullscreen();e.preventDefault();return;}
  if(e.key.toLowerCase()==='n'){$('#notes-button').click();e.preventDefault();return;}
  if(/BUTTON|A/.test(document.activeElement.tagName))return;
  if(['ArrowRight','PageDown',' '].includes(e.key)){show(current+1);e.preventDefault();}
  if(['ArrowLeft','PageUp'].includes(e.key)){show(current-1);e.preventDefault();}
  if(e.key==='Home'){show(0);e.preventDefault();}if(e.key==='End'){show(slides.length-1);e.preventDefault();}
  if(e.key.toLowerCase()==='f')slides[current].querySelector('.walk-next')?.click();
  if(e.key.toLowerCase()==='o')$('#overview-button').click();
 });
 addEventListener('hashchange',()=>show(fromHash(),false));addEventListener('resize',scale);
 addEventListener('beforeprint',()=>slides.forEach(s=>{s.inert=false;s.removeAttribute('aria-hidden');}));
 addEventListener('afterprint',()=>show(current,false));
 const slider=$('#metric-k');
 function updateMetrics(){
  const k=Number(slider.value),ranked=['X','A','Y','B','Z'].slice(0,k),gold=['A','B'];
  const rel=ranked.map(x=>gold.includes(x)?1:0),hit=rel.some(Boolean)?1:0,recall=rel.reduce((a,b)=>a+b,0)/2;
  const pos=rel.indexOf(1),mrr=pos<0?0:1/(pos+1),dcg=rel.reduce((v,r,i)=>v+r/Math.log2(i+2),0);
  const idcg=Array.from({length:Math.min(k,2)},(_,i)=>1/Math.log2(i+2)).reduce((a,b)=>a+b,0);
  $('#metric-k-label').textContent=k;
  $('#metric-live').textContent='Hit '+hit.toFixed(2)+' / Recall '+recall.toFixed(2)+' / MRR '+mrr.toFixed(2)+' / nDCG '+(dcg/idcg).toFixed(2);
  document.querySelectorAll('#rank-demo .rank').forEach((r,i)=>{r.classList.toggle('excluded',i>=k);r.children[2].textContent=i>=k?'제외':(['A','B'].includes(r.children[1].textContent)?'관련':'무관');});
  sendPresenter();
 }
 slider?.addEventListener('input',updateMetrics);if(slider)updateMetrics();
 const viewer=$('#image-viewer');
 document.querySelectorAll('figure').forEach(fig=>{const b=document.createElement('button');b.className='enlarge';b.textContent='그림 확대';b.setAttribute('aria-label',fig.querySelector('figcaption').textContent+' 확대');fig.append(b);b.onclick=()=>{const enlarged=fig.querySelector('img').cloneNode(true);enlarged.id='enlarged-image';$('#image-content').replaceChildren(enlarged);$('#image-caption').textContent=fig.querySelector('figcaption').textContent;$('#enlarged-image').style.filter=fig.classList.contains('external')?'grayscale(1)':'none';$('#image-content').classList.remove('zoomed');$('#image-zoom').setAttribute('aria-pressed','false');$('#image-zoom').textContent='원본 크기';viewer.showModal();};});
 $('#image-zoom').onclick=()=>{const zoomed=$('#image-content').classList.toggle('zoomed');$('#image-zoom').setAttribute('aria-pressed',String(zoomed));$('#image-zoom').textContent=zoomed?'화면에 맞춤':'원본 크기';};
 document.querySelectorAll('.diagram-walk').forEach(walk=>{const steps=JSON.parse(walk.dataset.walk);let stage=-1;const nodes=[...walk.querySelectorAll('.node')],caption=walk.querySelector('.walk-caption'),next=walk.querySelector('.walk-next'),back=walk.querySelector('.walk-back'),reset=walk.querySelector('.walk-reset');function focusStep(n){stage=n;walk.classList.toggle('is-stepping',n>=0);nodes.forEach((node,i)=>node.classList.toggle('walk-active',n>=0&&steps[n][0].includes(i)));caption.textContent=n<0?'전체 구조 · 흐름 보기를 눌러 설명 시작':`${n+1}/${steps.length} ${steps[n][1]} · ${steps[n][2]}`;back.disabled=n<0;reset.disabled=n<0;next.textContent=n<0?'흐름 보기':n===steps.length-1?'처음 단계':'다음 단계';sendPresenter();}next.onclick=()=>focusStep(stage===steps.length-1?0:stage+1);back.onclick=()=>focusStep(stage-1);reset.onclick=()=>focusStep(-1);});
 $('#image-close').onclick=()=>viewer.close();
 $('#overview').inert=true;scale();show(fromHash(),false);
 window.courseDeck={show,count:slides.length};
})();
