import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PRODUCTS = {
    "Astrox 100ZZ Dark Navy": "https://vsmash.com/product/yonex-astrox-100zz-dark-navy",
    "Astrox 100VA ZZ Grayish Beige": "https://vsmash.com/product/yonex-astrox-100va-zz-grayish-beige",
    "Yonex Power Cushion 65Z4 Men BR White": "https://vsmash.com/product/yonex-power-cushion-65z4-men-br-white",
}

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

    for name, url in PRODUCTS.items():
        page.goto(url, timeout=60000)
        page.wait_for_timeout(4000)

        buttons = page.query_selector_all("#productDetail button")

        for btn in buttons:
            if not btn.is_disabled():
                html = btn.inner_html().lower()

                if "bag" in html or "checkout" in html or "add" in html:
                    send_telegram(
                        f"🔥【有货提醒】\n{name}\n{url}"
                    )
                    break  # 同一个商品一次 run 只推一条

    browser.close()
