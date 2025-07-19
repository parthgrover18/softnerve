import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def clean_text(text):
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            cleaned_lines.append("")
        else:
            cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)

def scrape_chapter(url):
    
    if not url:
        raise ValueError("URL not found in .env file")

    output_path = "data/raw/chapter1.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        raw_content = page.locator('#mw-content-text').inner_text()
        content = clean_text(raw_content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        browser.close()
        print(f"Chapter content saved to {output_path}")

