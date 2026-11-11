/** Read-only rendering in an opaque sandbox; no access to the audience window. */
(() => {
 const protocol='llmops-week11-preview-v1',[session,slot]=location.hash.slice(1).split('~');
 const origin=location.protocol==='file:'?'*':location.origin,root=document.querySelector('#preview-root');
 let latest=0;
 function reply(type,extra={}){window.parent.postMessage({protocol,session,slot,type,...extra},origin);}
 addEventListener('message',async event=>{
  const data=event.data;
  if(event.source!==window.parent||event.origin!==(location.protocol==='file:'?'null':location.origin)||!data||data.protocol!==protocol||data.session!==session||data.slot!==slot||data.type!=='render'||typeof data.slide?.html!=='string')return;
  const revision=data.revision;latest=revision;
  const parsed=new DOMParser().parseFromString(data.slide.html,'text/html'),slide=parsed.querySelector('section.slide');
  if(!slide)return;
  slide.querySelectorAll('script,iframe,object,embed,base,link,style,.presenter-note,.enlarge').forEach(el=>el.remove());
  for(const el of [slide,...slide.querySelectorAll('*')])for(const attr of [...el.attributes]){
   if(/^on/i.test(attr.name)||attr.name==='srcdoc'||(/^(href|src|xlink:href)$/i.test(attr.name)&&/^\s*javascript:/i.test(attr.value)))el.removeAttribute(attr.name);
  }
  slide.classList.add('active');slide.removeAttribute('aria-hidden');root.replaceChildren(slide);
  document.title=data.slide.page+'쪽 · '+data.slide.title;
  await Promise.allSettled([document.fonts.ready,...[...slide.querySelectorAll('img')].map(img=>img.decode())]);
  if(revision!==latest)return;
  root.dataset.page=String(data.slide.page);root.dataset.revision=String(revision);
  reply('rendered',{revision,page:data.slide.page});
 });
 reply('ready');
})();
