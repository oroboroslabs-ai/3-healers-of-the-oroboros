This folder contains an SVG YouTube banner designed to match your HTML guide.

Files:
- youtube_banner.svg — 2560x1440 SVG with safe content centered in a 1235x338px area.

Guidance to export a PNG (2560x1440) ready for YouTube:

Windows (Inkscape CLI):
```
inkscape youtube_banner.svg --export-type=png --export-filename=youtube_banner.png --export-width=2560 --export-height=1440
```

ImageMagick (Windows: use `magick`):
```
magick -background none youtube_banner.svg -resize 2560x1440 -density 300 youtube_banner.png
```

Optimize to meet the file-size target (<= 0.98 MB):
- Use `pngquant` to lossy-optimize while keeping visual quality:
```
pngquant --quality=80-100 --speed=1 --output youtube_banner_opt.png --force youtube_banner.png
```
- Or use `oxipng` for lossless/level compression:
```
oxipng -o6 --strip all youtube_banner.png
```

Notes:
- The SVG keeps the Title, the three healers, and the oroboros ring within the centered safe area (1235x338). Badges and footer are placed outside the safe area.
- If you want me to export a PNG here (and attempt to hit <0.98 MB), say so — I can run headless tools if available, or produce an export script you can run locally.
