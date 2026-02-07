Blender-in-Docker banner render

This folder includes a Docker-based headless Blender setup to procedurally render a 2560x1440 YouTube banner with 3 stylized "AI female android MDs" and an Oroboros ring inside the YouTube safe area.

Files added:
- `Dockerfile` — image based on `blender:latest` that runs the script
- `render_banner_blender.py` — Blender Python (bpy) script that builds the scene and renders to `/output/blender_banner.png`
- `docker-compose.yml` — convenience compose file to build and run the container

How to run (local machine with Docker):

1. Create an `output` directory in this folder to receive renders:

```powershell
mkdir output
```

2. Build and run with Docker Compose (recommended):

```powershell
docker compose build --no-cache
docker compose run --rm blender-render
```

3. Or build & run with Docker manually:

```powershell
docker build -t blender-banner .
docker run --rm -v ${PWD}:/app -v ${PWD}\\output:/output blender-banner
```

Notes and limitations:
- This script produces simple, stylized characters (primitive shapes) — not photorealistic models. If you want custom character models, provide .blend assets or model files and I can update the script to import them.
- Rendering requires Blender inside Docker; ensure your Docker host has enough CPU/memory. For GPU rendering additional setup is required (NVIDIA runtime).
- If you want me to attempt to build and run the container here, say so — but the current environment may not have Docker available.

If you'd like higher detail (hair, clothing, facial features) I can either:
- import provided .blend/.obj files into the script (you supply), or
- generate more detailed geometry in the script (slower, larger render times).

Tell me whether to: build & run here (if possible), or provide modifications (pose, colors, text).