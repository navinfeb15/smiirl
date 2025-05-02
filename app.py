from playwright.sync_api import sync_playwright
import time, os


with sync_playwright() as pw:
    browser = pw.chromium.launch(
    headless=True,
    args=["--no-sandbox","--disable-setuid-sandbox","--disable-blink-features=AutomationControlled"]
)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)…",
        viewport={"width":1280,"height":720},
        locale="en-US"
    )
    context.add_init_script("""
    () => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
    window.navigator.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
    Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3] });
    }
    """)
    page = context.new_page()
    while True:
        page.goto("https://gamefound.com/en/projects/greymarsh-games-preben/sky-empire")
        page.wait_for_load_state()
        loc = page.locator(".gfu-project-summary-box__actions div strong")
        data = loc.text_content().strip() if loc.count() else 0
        smiirl_url = f"https://api.smiirl.com/e08e3c3b2963/set-number/639c0bebfbf909ae2d60293d494ce109/{data}"
        
        import requests
        requests.get(smiirl_url)
        # print(f"smirl updated - {data}")
        time.sleep(60)
