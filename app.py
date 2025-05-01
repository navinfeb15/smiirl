from flask import Flask, jsonify
from threading import Thread
from playwright.sync_api import sync_playwright
import time, os

app = Flask(__name__)
data = {"followers": 0}

def poll():
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
        page.goto("https://gamefound.com/en/projects/greymarsh-games-preben/sky-empire")
        page.wait_for_load_state()
        while True:
            loc = page.locator(".gfu-project-summary-box__actions div strong")
            data["followers"] = loc.text_content().strip() if loc.count() else 0
            time.sleep(60)

Thread(target=poll, daemon=True).start()

@app.route("/followers")
def followers():  # curl http://<ec2-ip>:5000/followers
    return jsonify(data)
