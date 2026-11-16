const fs=require('node:fs'),assert=require('node:assert/strict');
const {chromium}=require('../../.task-tools/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const errors=[],results=[],base='http://127.0.0.1:4173/';
 try {
 for(const width of [320,375,430,768,1024,1440,1920]){
  const p=await browser.newPage({viewport:{width,height:width<500?700:850},isMobile:width<500,hasTouch:width<500,reducedMotion:'reduce'});
  p.on('pageerror',e=>errors.push(e.message));
  let remote=0,connected=false,allDown=false,tileHosts=[];
  await p.route('https://**/*',r=>{
    const host=new URL(r.request().url()).hostname;remote++;tileHosts.push(host);
    if(!connected||allDown||host==='server.arcgisonline.com'&&p.url().includes('fallback'))return r.abort();
    return r.fulfill({status:200,contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256"><rect width="100%" height="100%" fill="#b8cfcd"/></svg>'});
  });
  const fit=async(label)=>{
    const layout=await p.evaluate(()=>({viewport:innerWidth,body:document.documentElement.scrollWidth,dialogs:[...document.querySelectorAll('dialog[open]')].map(e=>({width:e.getBoundingClientRect().width,content:e.scrollWidth,client:e.clientWidth}))}));
    assert(layout.body<=layout.viewport+1,JSON.stringify({width,label,layout}));
    assert(layout.dialogs.every(d=>d.width<=width&&d.content<=d.client+1),JSON.stringify({width,label,layout}));
  };
  for(const file of ['index.html','atlas.html','library.html','background.html','reader-apostles.html','reader-nicene.html','reader-athanasian.html']){
   await p.goto(base+file);await fit(file);
   assert.equal(await p.locator('.corner-nav-toggle').count(),1);
  }
  assert.equal(remote,0,'no startup network resources');
  await p.goto(base+'atlas.html');
  assert.equal(await p.locator('.v5-timeline li').count(),9);
  assert.equal(await p.locator('.v5-chains details').count(),6);
  for(let i=0;i<3;i++){
   await p.locator('.v5-chains summary').first().click();
   await p.locator('.v5-film summary').click();
   await p.locator('.culture-recall summary').first().click();
   await p.locator('.corner-nav-toggle').click();
   await fit('expanded interactive content');
   await p.locator('.corner-nav-toggle').click();
  }
  await p.locator('video').scrollIntoViewIfNeeded();
  await p.locator('video').evaluate(v=>v.play());
  assert(await p.locator('video').evaluate(v=>!v.paused&&v.duration>=23.9&&v.duration<=24.1));
  await p.locator('video').evaluate(v=>v.pause());
  // External tiles are simulated; no bulk tile requests.
  connected=true;
  await p.goto(base+'atlas.html?fallback');
  await p.locator('#map-load').click();
  await p.waitForFunction(()=>document.querySelector('#map-status').textContent.includes('在线底图已连接：OpenStreetMap'));
  assert(tileHosts.includes('server.arcgisonline.com')&&tileHosts.includes('tile.openstreetmap.org'));
  await p.selectOption('#map-provider','nasa');
  await p.waitForFunction(()=>document.querySelector('#map-status').textContent.includes('在线底图已连接：NASA'));
  assert(await p.locator('#nasa-date').isVisible());
  await p.locator('#nasa-date').fill('2026-11-11');
  await p.waitForFunction(()=>document.querySelector('#map-status').textContent.includes('在线底图已连接：NASA 近实时观测 · 2026-11-11'));
  await fit('online map and date');
  await p.locator('#map-unload').click();
  const before=remote;await p.selectOption('#map-provider','auto');await p.waitForTimeout(100);assert.equal(remote,before);
  allDown=true;await p.goto(base+'atlas.html?offline');await p.locator('#map-load').click();
  await p.waitForFunction(()=>document.querySelector('#map-status').textContent.includes('当前网络未能显示'));
  assert(await p.locator('.map').isVisible());assert(await p.locator('#map-retry').isVisible());
  allDown=false;await p.locator('#map-retry').click();await p.waitForFunction(()=>document.querySelector('#map-status').textContent.includes('在线底图已连接'));
  await p.locator('#map-unload').click();
  await p.goto(base+'index.html');
  const text=await p.locator('#a01 .core-thesis').textContent();
  await p.locator('#a01 .core-thesis').evaluate(el=>{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);document.dispatchEvent(new Event('pointerup'))});
  await p.locator('#mark-custom').click();
  await p.locator('[data-preset="distinction"]').click();
  await p.locator('input[name=bold]').check();await p.locator('input[name=fill]').check();
  await p.locator('select[name=lineColor]').selectOption('red');
  await p.locator('#mark-note').fill('分清本质与位格');
  await fit('note editor');
  await p.locator('.save-mark').click();
  await p.reload();
  assert.equal(await p.locator('#a01 .core-thesis').textContent(),text);
  const styled=p.locator('#a01 .note-bold.note-fill.note-dashed');
  assert(await styled.count());assert((await styled.first().getAttribute('style')).includes('note-line-red'));
  await p.locator('[data-notes-open]').first().click();
  await p.selectOption('#notes-filter','core');assert.equal(await p.locator('.personal-note-card:visible').count(),0);
  await p.selectOption('#notes-filter','distinction');assert.equal(await p.locator('.personal-note-card:visible').count(),1);
  await fit('filtered notes');
  if(width===375||width===1440){
   await p.locator('#notes-library [data-close-dialog]').click();await p.goto(base+'atlas.html');
   await p.locator('#evidence').scrollIntoViewIfNeeded();await p.screenshot({path:'qa/screenshots/v5-'+width+'.png'});
  }
  console.log('Passed viewport '+width);results.push({width,pages:7,expansionRepeats:3,mapFallbackAndRetry:true,video:true,notePersistence:true});
  await p.close();
 }
 assert.deepEqual(errors,[]);
 fs.writeFileSync('qa/v5-layout-report.json',JSON.stringify({results,errors,checked:new Date().toISOString()},null,2));
 console.log('V5 browser checks passed: '+results.map(r=>r.width).join(', '));
 } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});

