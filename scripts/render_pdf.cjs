const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
fs.mkdirSync(path.join(root,'qa'),{recursive:true});
(async () => {
 const macChrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
 const executablePath = process.env.CHROME_PATH || (fs.existsSync(macChrome) ? macChrome : undefined);
 const browser = await chromium.launch({headless:true,executablePath,args:['--allow-file-access-from-files']});
 const page = await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 const errors=[]; page.on('pageerror', e=>errors.push(e.message));
 const site=path.join(root,'dist/site');
 const checks=[];
 for (const width of [1440,390]) {
  await page.setViewportSize({width,height:1000});
  for(const filename of fs.readdirSync(site).filter(f=>f.endsWith('.html') && f!=='book.html')){
   await page.goto(pathToFileURL(path.join(site,filename)).href);
   await page.evaluate(async()=>{for(const img of document.images){img.loading='eager';await img.decode().catch(()=>{});}await document.fonts.ready;});
   const check=await page.evaluate(()=>({width:innerWidth,contentWidth:document.querySelector('main').getBoundingClientRect().width,overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),anchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href'))}));
   checks.push({filename,...check});
   if(['index.html','05-operation.html','07-china.html'].includes(filename)) await page.screenshot({path:path.join(root,`qa/${filename.replace('.html','')}-${width}.png`),fullPage:false});
  }
 }
 await page.goto(pathToFileURL(path.join(site,'05-operation.html')).href);
 await page.locator('#theme-toggle').click();
 const dark=await page.getAttribute('html','data-theme');
 await page.locator('#toc-toggle').click();
 const drawer=await page.locator('body').evaluate(e=>e.classList.contains('toc-open'));
 await page.keyboard.press('Escape');
 await page.evaluate(()=>localStorage.clear());
 await page.setViewportSize({width:1100,height:1000});
 for(const filename of fs.readdirSync(path.join(root,'assets/diagrams')).filter(f=>f.endsWith('.html'))){
  await page.goto(pathToFileURL(path.join(root,'assets/diagrams',filename)).href);
  await page.locator('svg').screenshot({path:path.join(root,'qa',filename.replace('.html','.png'))});
 }
 await page.goto(pathToFileURL(path.join(site,'book.html')).href);
 await page.evaluate(async()=>{document.documentElement.dataset.theme='light';for(const img of document.images){img.loading='eager';await img.decode();}await document.fonts.ready;});
 await page.emulateMedia({media:'print'});
 await page.evaluate(async()=>{await document.fonts.ready;});
 const pdf=path.join(site,'downloads/fdu-handbook.pdf');
 await page.pdf({path:pdf,format:'A4',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:8px;color:#777;width:100%;text-align:center;font-family:sans-serif">从 FDE 到 FDU · <span class="pageNumber"></span></div>',outline:true,tagged:true});
 fs.copyFileSync(pdf,path.join(root,'dist/fdu-handbook.pdf'));
 fs.writeFileSync(path.join(root,'qa/browser-checks.json'),JSON.stringify({checks,errors,themeToggle:dark==='dark',mobileDrawer:drawer},null,2));
 console.log(JSON.stringify({pagesChecked:checks.length,failures:checks.filter(c=>c.overflow||c.images.length||c.anchors.length||(c.width>900&&c.contentWidth<650)),errors,themeToggle:dark==='dark',mobileDrawer:drawer,pdf}));
 await browser.close();
})();
