const sharp = require('sharp');
const { execSync } = require('child_process');
const fs = require('fs');
(async ()=>{
  const svg = 'youtube_banner_medical.svg';
  const outPng = 'youtube_banner_medical.png';
  const outJpg = 'youtube_banner_medical.jpg';
  try{
    // Render PNG at exact size
    await sharp(svg)
      .resize(2560,1440)
      .png({compressionLevel:9, adaptiveFiltering:true})
      .toFile(outPng);
    console.log('Wrote', outPng);

    // Render high-quality JPEG
    await sharp(svg)
      .resize(2560,1440)
      .jpeg({quality:95, chromaSubsampling:'4:4:4'})
      .toFile(outJpg);
    console.log('Wrote', outJpg);

    const statPng = fs.statSync(outPng).size;
    console.log('PNG bytes:', statPng);

    const limit = 0.98 * 1024 * 1024;
    if(statPng > limit){
      console.log('PNG exceeds 0.98 MB — attempting pngquant optimization');
      // Try to run pngquant if installed
      try{
        // If pngquant not present, this will throw
        execSync('pngquant --version', {stdio: 'ignore'});
      }catch(e){
        console.log('pngquant not installed. Installing pngquant-bin...');
        execSync('npm install pngquant-bin --no-audit --no-fund', {stdio:'inherit'});
      }

      // Use the npm-installed binary path if available
      let pngquantBin = 'pngquant';
      try{
        const local = require('pngquant-bin');
        pngquantBin = local;
      }catch(e){
        // fallback to system pngquant
      }

      // Try progressively lower quality ranges until under limit
      const ranges = [['80','95'],['70','90'],['60','85']];
      let optimized = false;
      for(const r of ranges){
        const out = 'youtube_banner_medical.opt.png';
        const cmd = `${pngquantBin} --quality=${r[0]}-${r[1]} --speed 1 --output ${out} --force ${outPng}`;
        try{
          console.log('Running:', cmd);
          execSync(cmd, {stdio:'inherit'});
          const newSize = fs.statSync(out).size;
          console.log('Optimized size:', newSize);
          if(newSize <= limit){
            // replace original
            fs.renameSync(out, outPng);
            console.log('Optimization successful — file under limit. Saved as', outPng);
            optimized = true;
            break;
          } else {
            // keep the last optimized as backup
            fs.renameSync(out, 'youtube_banner_medical.opt'+r[0]+'.png');
          }
        }catch(e){
          console.error('pngquant failed for range', r, e.message);
        }
      }
      if(!optimized) console.log('Could not get PNG under limit with pngquant ranges tried. Consider JPEG or further manual tuning.');
    } else {
      console.log('PNG is already under limit.');
    }
  }catch(e){
    console.error('Error:', e);
    process.exit(1);
  }
})();