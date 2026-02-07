# Blender Dockerfile for headless rendering
ARG BLENDER_IMAGE=ghcr.io/blender/blender:stable
FROM ${BLENDER_IMAGE}

# Create app dir
WORKDIR /app

# Copy render script
COPY render_banner_blender.py /app/render_banner_blender.py

# Create output dir
RUN mkdir -p /output

# Default command: run the render script
CMD ["blender", "--background", "--python", "/app/render_banner_blender.py"]
