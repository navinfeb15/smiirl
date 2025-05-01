from flask import Flask, jsonify
from threading import Thread
from playwright.sync_api import sync_playwright
import time, os

app = Flask(__name__)
data = {"followers": 0}

def poll():
    with sync_playwright() as pw:
        page = pw.chromium.launch(headless=True, args=["--no-sandbox"]).new_page()
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
