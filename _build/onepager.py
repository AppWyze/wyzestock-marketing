"""Builds Wyzestock-One-Pager.pdf (A4) from _build/onepager.html with headless Chromium.

Run from the repo root:  python3 _build/onepager.py
Needs: pip install qrcode playwright (Chromium installed for Playwright).
"""
import asyncio
import io
from pathlib import Path

import qrcode
import qrcode.image.svg
from playwright.async_api import async_playwright

B = Path(__file__).parent
ROOT = B.parent


def qr_svg(url: str) -> str:
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=0)
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode()
    return svg[svg.index('<svg'):]


async def main():
    html = (B / 'onepager.html').read_text().replace('{{QR}}', qr_svg('https://wyzestock.co.za'))
    tmp = B / '_onepager_render.html'
    tmp.write_text(html)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(tmp.resolve().as_uri(), wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        await page.pdf(path=str(ROOT / 'Wyzestock-One-Pager.pdf'), format='A4', print_background=True,
                       margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        await page.set_viewport_size({'width': 794, 'height': 1123})
        await page.screenshot(path=str(B / '_onepager_preview.png'))
        await browser.close()
    tmp.unlink()
    print('wrote Wyzestock-One-Pager.pdf')


asyncio.run(main())
