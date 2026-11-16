/* Lightweight enhancements; existing theme and note storage remain compatible. */
(()=>{
  const form=document.querySelector('#mark-form');
  if(!form?.elements.lineColor)return;
  const presets={
    core:{color:'gold',bold:true,fill:true,underline:'solid'},
    distinction:{color:'blue',ink:true,underline:'dashed',lineColor:'purple'},
    review:{color:'green',block:true,underline:'dashed'}
  };
  const preview=document.querySelector('#mark-style-preview');
  form.querySelectorAll('[data-preset]').forEach(button=>{
    button.setAttribute('aria-pressed','false');
    button.onclick=()=>{
      const config=presets[button.dataset.preset];
      form.dataset.preset=button.dataset.preset;
      for(const k of ['bold','ink','fill','block'])form.elements[k].checked=!!config[k];
      for(const k of ['color','underline','lineColor'])form.elements[k].value=config[k]||'';
      form.dispatchEvent(new Event('change'));
    };
  });
  function previewExtra(){
    const color=form.elements.lineColor.value||form.elements.color.value;
    preview.style.setProperty('--mark-line','var(--note-line-'+color+')');
    form.querySelectorAll('[data-preset]').forEach(button=>button.setAttribute('aria-pressed',button.dataset.preset===form.dataset.preset));
  }
  form.addEventListener('change',previewExtra);
  new MutationObserver(previewExtra).observe(document.querySelector('#mark-editor'),{attributes:true,attributeFilter:['open']});
  const filter=document.querySelector('#notes-filter');
  const search=document.querySelector('#notes-search');
  function filterNotes(){
    const term=search.value.trim().toLowerCase();
    document.querySelectorAll('.personal-note-card').forEach(card=>{
      card.hidden=Boolean((term&&!card.textContent.toLowerCase().includes(term))||(filter.value&&card.dataset.preset!==filter.value));
    });
  }
  filter.addEventListener('change',filterNotes);
  search.addEventListener('input',filterNotes);
  document.querySelectorAll('video').forEach(video=>{
    if('IntersectionObserver' in window)new IntersectionObserver(entries=>{if(!entries[0].isIntersecting&&!video.paused)video.pause()}).observe(video);
    document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause()});
  });
})();

