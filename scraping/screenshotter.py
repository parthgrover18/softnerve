from playwright.sync_api import sync_playwright
import os
from math import ceil



def capture_scrolled_screenshots(url):

    if not url:
        raise ValueError("URL not found in .env file")

    output_dir = "data/screenshots"
    os.makedirs(output_dir, exist_ok=True)

    viewport_width = 1280
    viewport_height = 1000
    scroll_step = viewport_height - 40

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
        page.goto(url)
        page.wait_for_load_state("networkidle")

        total_height = page.evaluate("() => document.body.scrollHeight")
        num_screenshots = ceil(total_height / scroll_step)

        for i in range(num_screenshots):
            scroll_y = i * scroll_step
            page.evaluate(f"window.scrollTo(0, {scroll_y})")
            page.wait_for_timeout(500)

            filename = f"screenshot_part_{i + 1}.png"
            screenshot_path = os.path.join(output_dir, filename)
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Saved: {screenshot_path}")

        browser.close()

