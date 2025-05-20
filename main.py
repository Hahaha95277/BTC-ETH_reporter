import requests
from datetime import datetime
from telegram import Bot
from flask import Flask
import asyncio
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = Flask(__name__)

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    return float(response.json()['price'])

async def report_btc_eth_ratio():
    btc_price = get_price('BTCUSDT')
    eth_price = get_price('ETHUSDT')
    ratio = round(btc_price / eth_price, 2)
    today = datetime.now().strftime('%Y%m%d')
    message = f"{today}。BTC/ETH\n{int(btc_price)}/{int(eth_price)} = {ratio}"
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)
    print("訊息已送出！", message)

@app.route("/")
def index():
    return "BTC/ETH Reporter is running."

@app.route("/report")
def trigger_report():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(report_btc_eth_ratio())
    return "報告已送出！"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
