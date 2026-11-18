document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
  const filter=button.dataset.filter;
  document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  let count=0;
  document.querySelectorAll('.pub').forEach(p=>{p.hidden=filter!=='All'&&p.dataset.category!==filter;if(!p.hidden)count++;});
  const status=document.getElementById('filter-status');if(status)status.textContent=`${count} projects shown`;
}));
