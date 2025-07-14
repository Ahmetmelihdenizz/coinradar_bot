import os
import requests
import yfinance as yf

# Dosya yolları
BASE_DIR       = os.path.dirname(os.path.dirname(__file__))
COIN_LIST_FILE = os.path.join(BASE_DIR, 'coin_list.txt')
DATA_DIR       = os.path.join(BASE_DIR, 'data')

def fetch_top_100_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': False
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    coins = [c['symbol'].upper() + '-USD' for c in res.json()]
    with open(COIN_LIST_FILE, 'w') as f:
        for sym in coins:
            f.write(f"{sym}\n")
    print(f"✅ coin_list.txt oluşturuldu ({len(coins)} coin)")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def read_coin_list():
    with open(COIN_LIST_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_and_save_history(period='180d', interval='1d'):
    ensure_data_dir()
    for symbol in read_coin_list():
        print(f"⏳ {symbol} verisi çekiliyor…")
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if df.empty:
            print(f"⚠️  {symbol}: Veri bulunamadı.")
            continue
        out_path = os.path.join(DATA_DIR, f"{symbol}_hist.csv")
        df.to_csv(out_path)
        print(f"✔️  {symbol}: {len(df)} kayıt kaydedildi → {out_path}")

if __name__ == "__main__":
    fetch_top_100_coins()
    fetch_and_save_history()
