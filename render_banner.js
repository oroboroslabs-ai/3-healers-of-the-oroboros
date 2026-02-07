const puppeteer = require('puppeteer');
const path = require('path');
(async ()=>{
  const browser = await puppeteer.launch({args:['--no-sandbox','--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setViewport({width:2560,height:1440});
  const file = 'file://' + path.resolve('youtube-banner-simple2.html').replace(/\\/g, '/');
  await page.goto(file, {waitUntil: 'networkidle0'});
  await new Promise(resolve => setTimeout(resolve, 600));
  await page.screenshot({path: 'youtube_banner_render.png', fullPage: false});
  await browser.close();
  console.log('Rendered to youtube_banner_render.png');
})();