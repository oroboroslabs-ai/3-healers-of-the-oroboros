const sharp = require('sharp');
const fs = require('fs');
(async ()=>{
  try{
    const input = './output/blender_banner.png';
    const overlay = 'overlay_safe_area.svg';
    if(!fs.existsSync(input)){
      console.error('Input render not found:', input); process.exit(1);
    }

    // Composite SVG overlay onto render
    await sharp(input)
      .composite([{ input: overlay, blend: 'over' }])
      .png({compressionLevel:9})
      .toFile('youtube_banner_final.png');
    console.log('Wrote youtube_banner_final.png');

    // Also output high-quality JPEG
    await sharp('youtube_banner_final.png')
      .jpeg({quality:95, chromaSubsampling:'4:4:4'})
      .toFile('youtube_banner_final.jpg');
    console.log('Wrote youtube_banner_final.jpg');

    // Show sizes
    const s1 = fs.statSync('youtube_banner_final.png').size;
    const s2 = fs.statSync('youtube_banner_final.jpg').size;
    console.log('PNG bytes:', s1, 'JPG bytes:', s2);
  }catch(e){
    console.error(e);
    process.exit(1);
  }
})();