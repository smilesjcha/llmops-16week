(() => {
  document.documentElement.classList.add('js');
  const $=s=>document.querySelector(s), notes=[...document.querySelectorAll('.page-note')], all=[...document.querySelectorAll('details')];
  const texts=new Map(notes.map(n=>[n,n.textContent.toLocaleLowerCase()]));
  function filter(){
    const query=$('#search').value.trim().toLocaleLowerCase(), priority=$('#priority').value;
    notes.forEach(n=>n.hidden=!(texts.get(n).includes(query)&&(!priority||n.dataset.priority===priority)));
    document.querySelectorAll('.page-group').forEach(g=>g.hidden=![...g.querySelectorAll('.page-note')].some(n=>!n.hidden));
    $('#search-status').textContent=`64쪽 중 ${notes.filter(n=>!n.hidden).length}쪽 표시`;
  }
  $('#search').addEventListener('input',filter);$('#priority').addEventListener('change',filter);
  $('#expand').onclick=()=>notes.filter(n=>!n.hidden).forEach(n=>n.open=true);
  $('#collapse').onclick=()=>all.forEach(n=>n.open=false);
  $('#print').onclick=()=>window.print();
  function locate(){
    const target=document.getElementById(location.hash.slice(1));
    if(target?.matches('details')){
      if(target.hidden||target.closest('[hidden]')){$('#search').value='';$('#priority').value='';filter();}
      target.open=true;requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
    }
  }
  window.addEventListener('hashchange',locate);
  document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(a&&a.hash===location.hash)locate();});
  let printState=[];
  window.addEventListener('beforeprint',()=>{printState=all.map(n=>n.open);all.forEach(n=>n.open=true);});
  window.addEventListener('afterprint',()=>all.forEach((n,i)=>n.open=printState[i]??false));
  filter();locate();
})();
