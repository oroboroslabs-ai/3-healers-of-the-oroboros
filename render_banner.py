#!/usr/bin/env python3
"""
Render the YouTube banner HTML to a JPG image
"""
import asyncio
import sys
from pathlib import Path

async def render_html_to_jpg():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Installing Playwright...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        from playwright.async_api import async_playwright
    
    html_path = Path(r"j:\oroboros-programs\3-Healers_of_the_Oroboros\youtube_banner.html")
    output_path = Path(r"j:\oroboros-programs\3-Healers_of_the_Oroboros\youtube_banner.jpg")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 2560, "height": 1440})
        
        # Load the HTML file
        await page.goto(f"file:///{html_path}")
        
        # Give it a moment to render
        await page.wait_for_load_state("networkidle")
        
        # Take a screenshot as JPG with compression
        await page.screenshot(
            path=str(output_path),
            type="jpeg",
            quality=85,
            full_page=False
        )
        
        await browser.close()
        
        # Check file size
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"✓ Banner rendered successfully!")
        print(f"  Location: {output_path}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print(f"  Dimensions: 2560x1440")

if __name__ == "__main__":
    asyncio.run(render_html_to_jpg())
