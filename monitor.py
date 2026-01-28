import time
import os
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PRODUCTS = {
    "Astrox 100ZZ Dark Navy": "https://vsmash.com/product/yonex-astrox-100zz-dark-navy",
    "Astrox 100VA ZZ Grayish Beige": "https://vsmash.com/product/yonex-astrox-100va-zz-grayish-beige",
}

SELECTOR = (
    "#productDetail button"
)

def send_telegram(msg):
    import requests
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data, timeout=10)

already_notified = set()

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

    page = browser.new_page()

    while True:
        for name, url in PRODUCTS.items():
            if name in already_notified:
                continue

            try:
                page.goto(url, timeout=60000)
                page.wait_for_timeout(4000)

                btn = page.query_selector(SELECTOR)

                if btn:
                    text = btn.inner_text().lower()
                    disabled = btn.is_disabled()

                    if ("add" in text or "bag" in text) and not disabled:
                        send_telegram(f"🔥 {name} 补货了！\n{url}")
                        already_notified.add(name)

            except Exception as e:
                print("Error:", e)

        time.sleep(300)
