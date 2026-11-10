(() => {
 const slides=[...document.querySelectorAll('.slide')], $=s=>document.querySelector(s);
 let current=0,previousFocus=null;
 function scale(){document.documentElement.style.setProperty('--scale',String(Math.min(1,(innerWidth-32)/1440,(innerHeight-110)/810)));}
 function show(n,update=true){
  current=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',i===current?'false':'true');s.inert=i!==current;});
  $('#status').textContent=(current+1)+' / '+slides.length;$('#jump').value=current+1;
  $('#previous').disabled=current===0;$('#next').disabled=current===slides.length-1;
  $('#notes-text').textContent=slides[current].querySelector('.presenter-note').textContent;
  if(update)history.replaceState(null,'','#slide-'+(current+1));
 }
 function fromHash(){const n=Number(location.hash.replace('#slide-',''));return Number.isFinite(n)&&n>0?n-1:0;}
 document.documentElement.classList.add('js');
 $('#previous').onclick=()=>show(current-1);$('#next').onclick=()=>show(current+1);
 $('#jump').onchange=()=>show(Number($('#jump').value)-1);
 function closeOverview(){$('#overview').classList.remove('open');$('#overview').inert=true;previousFocus?.focus();}
 $('#overview-button').onclick=()=>{previousFocus=document.activeElement;$('#overview').inert=false;$('#overview').classList.add('open');$('#overview-close').focus();};
 $('#overview-close').onclick=closeOverview;
 $('.overview-list').innerHTML=slides.map((s,i)=>'<button data-slide="'+i+'">'+String(i+1).padStart(2,'0')+'　'+s.querySelector('h1,h2').textContent+'</button>').join('');
 $('.overview-list').onclick=e=>{const b=e.target.closest('[data-slide]');if(b){show(Number(b.dataset.slide));closeOverview();}};
 $('#notes-button').onclick=()=>{const opened=$('#notes-panel').classList.toggle('open');$('#notes-button').setAttribute('aria-expanded',String(opened));};
 $('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{$('#status').textContent='전체화면 미지원';}};
 $('#print').onclick=()=>window.print();
 addEventListener('keydown',e=>{
  if($('#image-viewer').open)return;
  if($('#overview').classList.contains('open')){
   if(e.key==='Escape'){closeOverview();e.preventDefault();}
   if(e.key==='Tab'){const items=[...$('#overview').querySelectorAll('button')],first=items[0],last=items.at(-1);if(e.shiftKey&&document.activeElement===first){last.focus();e.preventDefault();}else if(!e.shiftKey&&document.activeElement===last){first.focus();e.preventDefault();}}
   return;
  }
  if(/INPUT|SELECT|TEXTAREA|BUTTON|A/.test(document.activeElement.tagName))return;
  if(['ArrowRight','PageDown',' '].includes(e.key)){show(current+1);e.preventDefault();}
  if(['ArrowLeft','PageUp'].includes(e.key)){show(current-1);e.preventDefault();}
  if(e.key==='Home'){show(0);e.preventDefault();}if(e.key==='End'){show(slides.length-1);e.preventDefault();}
  if(e.key.toLowerCase()==='n')$('#notes-button').click();
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
 }
 slider?.addEventListener('input',updateMetrics);if(slider)updateMetrics();
 const viewer=$('#image-viewer');
 document.querySelectorAll('figure').forEach(fig=>{const b=document.createElement('button');b.className='enlarge';b.textContent='그림 확대';b.setAttribute('aria-label',fig.querySelector('figcaption').textContent+' 확대');fig.append(b);b.onclick=()=>{const enlarged=fig.querySelector('img').cloneNode(true);enlarged.id='enlarged-image';$('#image-content').replaceChildren(enlarged);$('#image-caption').textContent=fig.querySelector('figcaption').textContent;$('#enlarged-image').style.filter=fig.classList.contains('external')?'grayscale(1)':'none';viewer.showModal();};});
 $('#image-close').onclick=()=>viewer.close();
 $('#overview').inert=true;scale();show(fromHash(),false);
 window.courseDeck={show,count:slides.length};
})();
