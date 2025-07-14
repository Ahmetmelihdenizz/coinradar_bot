import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    pass

BASE_DIR       = os.path.dirname(os.path.dirname(__file__))
PERF_FILE      = os.path.join(BASE_DIR, 'performance.csv')
OUTPUT_DIR     = os.path.join(BASE_DIR, 'outputs')
LAST_RECS_FILE = os.path.join(OUTPUT_DIR, 'today.xlsx')

def load_last_recs():
    return pd.read_excel(LAST_RECS_FILE)

def fetch_close_price(symbol: str, date: dt.date) -> float:
    from src.indicators import load_history
    df = load_history(symbol)
    if str(date) not in df.index:
        raise ValueError(f"{symbol} için {date} günü verisi yok.")
    return df.loc[str(date), 'Close']

def get_yesterday(today: dt.date) -> dt.date:
    if today.weekday() == 0:
        return today - dt.timedelta(days=3)
    elif today.weekday() == 6:
        return today - dt.timedelta(days=2)
    else:
        return today - dt.timedelta(days=1)

def update_performance():
    recs = load_last_recs()
    today     = dt.date.today()
    yesterday = get_yesterday(today)

    rows = []
    portfoy_kar = 0.0
    for _, row in recs.iterrows():
        sym = row['symbol']
        try:
            open_price  = fetch_close_price(sym, yesterday)
            close_price = fetch_close_price(sym, today)
            ret = (close_price / open_price - 1)
            success = int(ret >= 0.025)
            kar = ret * 10000  # 10K yatırımla günlük net kâr
            portfoy_kar += kar
        except Exception as e:
            print(f"[ERROR] {sym}: {e}")
            continue
        rows.append({'date': yesterday, 'symbol': sym, 'return_%': ret*100, 'success': success, 'kar': kar})

    perf_df = pd.DataFrame(rows)
    if os.path.exists(PERF_FILE):
        old = pd.read_csv(PERF_FILE, parse_dates=['date'])
        perf_df = pd.concat([old, perf_df], ignore_index=True)

    perf_df['date'] = pd.to_datetime(perf_df['date'], errors='coerce')
    perf_df.to_csv(PERF_FILE, index=False)
    print(f"✔️ performance.csv güncellendi: toplam {len(perf_df)} kayıt")
    cutoff = today - dt.timedelta(days=30)
    last30 = perf_df[perf_df['date'] >= pd.to_datetime(cutoff)]
    success_rate = last30['success'].mean() * 100
    avg_return   = last30['return_%'].mean()
    print(f"📈 Son 30 günlük başarı oranı: %{success_rate:.2f}, ort. günlük getiri: %{avg_return:.2f}")
    print(f"💰 Portföy günlük toplam kâr: {portfoy_kar:.2f}₺")

    if not last30.empty:
        fig, ax = plt.subplots()
        last30.groupby('date')['success'].mean().plot(ax=ax)
        ax.set_title('Son 30 Günlük Başarı Oranı')
        ax.set_ylabel('Başarı Oranı')
        ax.set_xlabel('Tarih')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    update_performance()
