from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time
import datetime
import requests

app = Flask(__name__)

# بيانات تسجيل الدخول إلى Pocket Option
PO_EMAIL = "your_email@example.com"
PO_PASSWORD = "your_password"

# إعدادات التداول الافتراضية
TRADE_AMOUNT = "1"
TRADE_DURATION = "60"  # ثانية (60 = دقيقة واحدة)

# بيانات البوت في Telegram
BOT_TOKEN = "ضع_هنا_توكن_البوت"
CHAT_ID = "8188186011"

# إعداد المتصفح (بدون واجهة رسومية)
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# تسجيل الدخول وتنفيذ صفقة
def execute_trade(action, asset="EURUSD"):
    driver = get_driver()
    driver.get("https://pocketoption.com/en/login/")

    time.sleep(3)
    driver.find_element(By.NAME, "email").send_keys(PO_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PO_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(5)
    driver.get("https://pocketoption.com/en/platform/")

    time.sleep(7)  # تحميل المنصة

    try:
        amount_input = driver.find_element(By.CSS_SELECTOR, "input.amount-input")
        amount_input.clear()
        amount_input.send_keys(TRADE_AMOUNT)

        if action.lower() == "buy":
            driver.find_element(By.CSS_SELECTOR, "button[class*='up']").click()
        else:
            driver.find_element(By.CSS_SELECTOR, "button[class*='down']").click()

        print(f"✅ Executed {action.upper()} trade at {datetime.datetime.now()}")
        time.sleep(5)

    except Exception as e:
        print("❌ Error during trade:", e)

    finally:
        driver.quit()

@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_data(as_text=True)
    parsed = {}
    for line in data.split("\n"):
        if ':' in line:
            key, value = line.split(':', 1)
            parsed[key.strip().lower()] = value.strip()

    action = parsed.get("action", "buy")
    asset = parsed.get("symbol", "EURUSD")
    price = parsed.get("price", "Market")
    timeframe = parsed.get("timeframe", "1m")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # إرسال رسالة إلى Telegram
    message = f"""
━━━━━━━━━━━━━━━━━━━
📊 *VETAJ SIGNAL*

🔔 *TYPE:* `{action.upper()}`
💱 *PAIR:* `{asset}`
💵 *PRICE:* `{price}`
⏱️ *TIMEFRAME:* `{timeframe}`
🕒 *TIME:* `{now}`
━━━━━━━━━━━━━━━━━━━
"""
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })

    threading.Thread(target=execute_trade, args=(action, asset)).start()
    return f"✅ Trade signal received: {action} on {asset}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
