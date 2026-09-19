import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright


async def capture(url: str, output: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        await page.goto(url, wait_until="networkidle")
        await page.screenshot(path=output, full_page=True)

        await browser.close()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python capture_screenshot.py <url> [output.png]")
        raise SystemExit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"

    Path(output).parent.mkdir(parents=True, exist_ok=True)

    asyncio.run(capture(url, output))
    print(f"Screenshot saved: {output}")


if __name__ == "__main__":
    main()