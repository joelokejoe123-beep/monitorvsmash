import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 用一个【确定有货】的商品来验证
NAME = "Astrox 100ZZ Kurenai (TEST)"
URL = "https://vsmash.com/product/yonex-astrox-100zz-kurenai"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data, timeout=10)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page()

    page.goto(URL, timeout=60000)
    page.wait_for_timeout(4000)

    buttons = page.query_selector_all("#productDetail button")

    for btn in buttons:
        if not btn.is_disabled():
            html = btn.inner_html().lower()
            if "bag" in html or "checkout" in html or "add" in html:
                send_telegram(f"✅【验证成功】{NAME} 检测为有货\n{URL}")
                break

    browser.close()
