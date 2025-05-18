# Skhni Telegram Trading Signal Bot

This bot receives trading signals (via webhook) and sends them to a Telegram chat.

## How to Use

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python main.py
   ```

3. Send a POST request to `/signal` with this format:
   ```
   action:buy
   symbol:BTCUSDT
   price:64000
   timeframe:5m
   ```

## Made for @Skhni_bot
