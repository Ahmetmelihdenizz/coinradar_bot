import os
from typing import List
import pandas as pd
from src.predictor import predict
from src.scorer import compute_score

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_TECH_SCORE = 50
TOP_N = 5

TARGET_RETURN    = 0.027   # %2.7 brüt (net %2.5)
COMMISSION_RATE  = 0.002   # %0.2 toplam
MIN_DAILY_PROFIT = 250     # ₺

def read_coin_list() -> List[str]:
    data_dir = os.path.join(BASE_DIR, "data")
    return sorted(f.split("_")[0] for f in os.listdir(data_dir) if f.endswith("_indicators.csv"))

def get_recommendations(invest_amount: float = 10000.0) -> (pd.DataFrame, bool):
    records = []
    for sym in read_coin_list():
        try:
            prob = predict(sym)
        except Exception:
            continue
        score = compute_score(prob, DEFAULT_TECH_SCORE)
        gross = prob * invest_amount * TARGET_RETURN
        commission = invest_amount * COMMISSION_RATE
        net = round(gross - commission, 2)
        records.append({'symbol': sym, 'prob': prob, 'score': score, 'net_profit': net})

    df_all = pd.DataFrame(records)
    if df_all.empty:
        return df_all, False
    df_ok = df_all[df_all['net_profit'] >= MIN_DAILY_PROFIT]
    if not df_ok.empty:
        return df_ok.sort_values('score', ascending=False).head(TOP_N).reset_index(drop=True), True
    return df_all.sort_values('score', ascending=False).head(TOP_N).reset_index(drop=True), False

if __name__ == '__main__':
    recs, ok = get_recommendations(10000)
    if not ok:
        print(f"⚠️ Hiç coin ₺{MIN_DAILY_PROFIT} net kâr eşiklerini geçemedi, yine de en iyi {TOP_N} öneri:")
    else:
        print(f"🔔 Günün Önerileri (₺10.000 yatırımla, komisyon sonrası net kâr ≥ ₺{MIN_DAILY_PROFIT}):")
    for i, r in recs.iterrows():
        print(f"{i+1}. {r['symbol']} — Net Kâr: {r['net_profit']} ₺ "
              f"(P={r['prob']:.3f}, Score={r['score']})")
