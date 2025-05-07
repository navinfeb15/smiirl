import logging
import time
import requests
from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError

# logging setup
logging.basicConfig(
    filename='script.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def init_playwright():
    pw = sync_playwright().start()
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
    return pw, browser, context, page

# initialize
pw, browser, context, page = init_playwright()
count = "0"
url = "https://gamefound.com/en/projects/greymarsh-games-preben/sky-empire"
smiirl_base = "https://api.smiirl.com/e08e3c3b2963/set-number/639c0bebfbf909ae2d60293d494ce109"

while True:
    try:
        response = page.goto(url, timeout=30000, wait_until="load")
        if response and response.status == 200:
            loc = page.locator(".gfu-project-summary-box__actions div strong")
            data = loc.text_content().strip() if loc.count() else count
            requests.get(f"{smiirl_base}/{data}")
            count = data
        else:
            logging.error(f"Page load failed with status: {response.status if response else 'no response'}")
    except TimeoutError:
        #logging.error("Page.goto timeout – restarting Playwright")
        browser.close()
        pw.stop()
        pw, browser, context, page = init_playwright()
    except Exception as e:
        logging.exception(f"Unexpected loop error: {e}")
    time.sleep(60)
