import os
import pandas as pd
import joblib
from src.indicators import compute_indicators

BASE_DIR   = os.path.dirname(os.path.dirname(__file__))
MODEL_FILE = os.path.join(BASE_DIR, 'models', 'model.pkl')

def load_model():
    model = joblib.load(MODEL_FILE)
    print(f"[predictor] Model loaded from {MODEL_FILE}")
    return model

def predict(symbol: str) -> float:
    try:
        df = compute_indicators(symbol)
        if df is None or df.empty:
            raise ValueError("compute_indicators returned empty DataFrame")
        latest = df.tail(1)
        model = load_model()
        feat_names = model.get_booster().feature_names
        X = latest[feat_names]
        if X.isnull().any().any():
            raise ValueError(f"NaN in features for {symbol}")
        prob = model.predict_proba(X)[0][1]
        print(f"[predictor] {symbol} prob = {prob:.4f}")
        return prob
    except Exception as e:
        print(f"[predictor][ERROR] {symbol}: {e}")
        return 0.0

if __name__ == "__main__":
    symbol = "BTC-USD"
    prob = predict(symbol)
    print(f"{symbol} → probability of >%2.5 gain: {prob:.4f}")
