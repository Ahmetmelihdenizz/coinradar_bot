import os
import pandas as pd
from indicators import compute_indicators

BASE_DIR       = os.path.dirname(os.path.dirname(__file__))
COIN_LIST_FILE = os.path.join(BASE_DIR, 'coin_list.txt')
DATA_DIR       = os.path.join(BASE_DIR, 'data')
DATASET_FILE   = os.path.join(BASE_DIR, 'ml_dataset.csv')

def read_coin_list() -> list[str]:
    with open(COIN_LIST_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def build_features(symbol: str) -> pd.DataFrame | None:
    csv_path = os.path.join(DATA_DIR, f"{symbol}_hist.csv")
    if not os.path.exists(csv_path):
        print(f"⚠️  {symbol}: Veri dosyası bulunamadı, atlanıyor.")
        return None

    try:
        df = compute_indicators(symbol)
    except Exception as e:
        print(f"⚠️  {symbol}: İndikatör hesaplanırken hata ({e}), atlanıyor.")
        return None

    df = df.copy()
    df['return_1d'] = df['Close'].shift(-1) / df['Close'] - 1
    df['return_2d'] = df['Close'].shift(-2) / df['Close'] - 1
    df['label_1d']  = (df['return_1d'] > 0.025).astype(int)
    df['label_2d']  = (df['return_2d'] > 0.035).astype(int)
    df = df.iloc[:-2]
    df['symbol'] = symbol
    return df

def main():
    symbols = read_coin_list()
    all_dfs = []
    for sym in symbols:
        print(f"⏳ {sym} için feature oluşturuluyor…")
        feat = build_features(sym)
        if feat is not None:
            all_dfs.append(feat)
    if not all_dfs:
        print("❌ Hiç veri işlenmedi, ml_dataset.csv oluşturulamadı.")
        return
    dataset = pd.concat(all_dfs, axis=0)
    dataset.to_csv(DATASET_FILE, index=True)
    print(f"✔️ ml_dataset.csv oluşturuldu: {dataset.shape[0]} satır × {dataset.shape[1]} sütun")

if __name__ == "__main__":
    main()
