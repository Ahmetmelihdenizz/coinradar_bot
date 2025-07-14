import os
import pandas as pd
import ta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_history(symbol: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, f"{symbol}_hist.csv")
    df = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
        date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce')
    )
    cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    df.dropna(subset=['Close'], inplace=True)
    return df

def add_rsi(df, period=14):      return ta.momentum.RSIIndicator(df['Close'], window=period).rsi().rename('rsi')
def add_macd(df):                return ta.trend.MACD(df['Close']).macd().rename('macd')
def add_macd_signal(df):         return ta.trend.MACD(df['Close']).macd_signal().rename('macd_signal')
def add_bollinger_high(df):      return ta.volatility.BollingerBands(df['Close']).bollinger_hband().rename('bb_h')
def add_bollinger_low(df):       return ta.volatility.BollingerBands(df['Close']).bollinger_lband().rename('bb_l')
def add_adx(df, period=14):      return ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'], window=period).adx().rename('adx')
def add_ma_short(df, n=5):       return df['Close'].rolling(n).mean().rename('ma_short')
def add_ma_long(df, n=20):       return df['Close'].rolling(n).mean().rename('ma_long')
def add_ma_diff(df):             return (df['Close'].rolling(5).mean() - df['Close'].rolling(20).mean()).rename('ma_diff')
def add_volatility(df, window=14): return df['Close'].pct_change().rolling(window).std().rename('volatility')
def add_vol_spike(df):           return df['Volume'].pct_change().rename('vol_spike')
def add_momentum(df, period=3):  return df['Close'].pct_change(periods=period).rename('momentum_3d')
def add_atr(df, period=14):      return ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close'], window=period).average_true_range().rename('atr')
def add_roc(df, period=10):      return ta.momentum.ROCIndicator(df['Close'], window=period).roc().rename('roc')
def add_obv(df):                 return ta.volume.OnBalanceVolumeIndicator(df['Close'], df['Volume']).on_balance_volume().rename('obv')

def compute_indicators(symbol: str) -> pd.DataFrame:
    df = load_history(symbol)
    df['rsi'] = add_rsi(df)
    df['macd'] = add_macd(df)
    df['macd_signal'] = add_macd_signal(df)
    df['bb_h'] = add_bollinger_high(df)
    df['bb_l'] = add_bollinger_low(df)
    df['adx'] = add_adx(df)
    df['ma_short'] = add_ma_short(df)
    df['ma_long'] = add_ma_long(df)
    df['ma_diff'] = add_ma_diff(df)
    df['volatility'] = add_volatility(df)
    df['vol_spike'] = add_vol_spike(df)
    df['momentum_3d'] = add_momentum(df)
    df['atr'] = add_atr(df)
    df['roc'] = add_roc(df)
    df['obv'] = add_obv(df)
    df.dropna(inplace=True)
    out_path = os.path.join(DATA_DIR, f"{symbol}_indicators.csv")
    df.to_csv(out_path)
    return df

if __name__ == "__main__":
    df = compute_indicators("BTC-USD")
    print(df.tail())
