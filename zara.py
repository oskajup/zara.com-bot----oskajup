import time
import random
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = "8900548662:AAFGzGp22FdxK2Y6TIobJcac3P7V2SNV3FU" # paste your telegram tocken
CHAT_ID = "7200041211" # paste your chat id from telegram

PRODUCTS = { # here you can paste url to particular clothes and the size of them you're looking for
    # example:
    "https://www.zara.com/pl/pl/leather-bomber-jacket-p00624401.html?v1=529062252": ["L"],
    "https://www.zara.com/pl/pl/basic-hoodie-p00761370.html?v1=496783639": ["L"]
    }

def send_telegram_msg(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Błąd Telegram: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    page = context.new_page()
    print("Script running")

    while True:
        for url, desired_sizes in PRODUCTS.items():
            try:
                page.goto(url, wait_until="domcontentloaded")
                time.sleep(1) 
                
                cookie_btn = page.query_selector('button#onetrust-accept-btn-handler')
                if cookie_btn:
                    cookie_btn.click()
                    print("✅ Accepted cookies.")
                    time.sleep(1)

                # if you're not from Poland paste here the code from Inspect of button
                btn_select = page.query_selector('button[aria-label^="Dodaj"]:not([aria-label^="Dodaj element"])')
                
                #btn_select = page.query_selector('button[aria-label^="Add"]:not([aria-label^="Add element"])')

                if btn_select:
                    btn_select.click(force=True)
                    print("✅ Pressed Dodaj/Add button.")
                    time.sleep(1)
                else:
                    print("❌ button not found")

                all_size_buttons = page.query_selector_all('button.size-selector-sizes-size__button')
                
                found_sizes = []
                print(f"DEBUG: Found {len(all_size_buttons)} buttons.")
                
                for btn in all_size_buttons:
                    label_el = btn.query_selector('[data-qa-qualifier="size-selector-sizes-size-label"]')
                    if not label_el:
                        continue
                    
                    size_text = label_el.inner_text().strip().upper()
                    status = btn.get_attribute('data-qa-action')
                    
                    if status == 'size-in-stock':
                        print(f"DEBUG: Size {size_text} is AVAILABLE")
                        if size_text in [s.upper() for s in desired_sizes]:
                            found_sizes.append(size_text)
                    elif status == 'size-out-of-stock':
                        print(f"DEBUG: Size {size_text} is UNAVAILABLE")
                
                if found_sizes:
                    msg = f"🎉 AVAILABLE! \n Product: {url} \nSizes: {', '.join(found_sizes)}"
                    print(msg)
                    send_telegram_msg(msg)
                else:
                    print(f"❌ No desired sizes for: {url}")

            except Exception as e:
                print(f"⚠️ Error at {url}: {e}")
            
            # time sleep between searching the next item from the dict (random between 2-3 sec.)
            time.sleep(random.uniform(2,3))

        # time sleep between searching the same items again (random between 20-45 sec.)
        l = time.sleep(random.uniform(20, 45))