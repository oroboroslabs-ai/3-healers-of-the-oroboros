const sharp = require('sharp');
(async ()=>{
  try{
    await sharp('youtube_banner_render.png')
      .jpeg({quality:95, chromaSubsampling:'4:4:4'})
      .toFile('youtube_banner_highq.jpg');
    console.log('Wrote youtube_banner_highq.jpg');
  }catch(e){
    console.error(e);
    process.exit(1);
  }
})();