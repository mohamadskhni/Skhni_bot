from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

# بيانات البوت
BOT_TOKEN = "7117692959:AAFLQxcCrp8I4VFd3PI_5rGyDN3C5zCKKDI"
CHAT_ID = "8188186011"

@app.route('/')
def home():
    return "✅ Skhni_bot is online!"

@app.route('/signal', methods=['POST'])
def signal():
    data = request.get_data(as_text=True)
    parsed = {}
    for line in data.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            parsed[key.strip().lower()] = value.strip()

    message = f"""
━━━━━━━━━━━━━━━━━━━
📊 *VETAJ SIGNAL*

🔔 *TYPE:* `{parsed.get('action', 'BUY')}`
💱 *PAIR:* `{parsed.get('symbol', 'BTCUSDT')}`
💵 *PRICE:* `{parsed.get('price', 'Market')}`
⏱️ *TIMEFRAME:* `{parsed.get('timeframe', '1m')}`
🕒 *TIME:* `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
━━━━━━━━━━━━━━━━━━━
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    )

    return "✅ Signal Sent"
