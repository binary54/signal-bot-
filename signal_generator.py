import pandas as pd
import numpy as np
import requests
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from datetime import datetime

# ======= CONFIGURATION =======
PAIR = "EUR/USD"
INTERVAL = "1min"
API_KEY = "demo"  # Replace with real API key if you have one
# =============================

url = f"https://api.twelvedata.com/time_series?symbol={PAIR}&interval={INTERVAL}&outputsize=30&apikey={API_KEY}"

response = requests.get(url)
data = response.json()

if "values" not in data:
    print("❌ Error: Data not received properly. Check API or Pair.")
    exit()

df = pd.DataFrame(data['values'])
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')
df['close'] = df['close'].astype(float)

df['EMA5'] = EMAIndicator(close=df['close'], window=5).ema_indicator()
df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()

last = df.iloc[-1]
prev = df.iloc[-2]

if last['close'] > last['EMA5'] and last['RSI'] > 50:
    signal = "CALL"
elif last['close'] < last['EMA5'] and last['RSI'] < 50:
    signal = "PUT"
else:
    signal = "NO SIGNAL"

signal_time = datetime.now().strftime('%H:%M')
print(f"\n📡 Signal: {signal_time};{PAIR};{signal}\n")
