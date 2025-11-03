import numpy as np
import pandas as pd


def rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff()
    up, down = delta.clip(lower=0), -delta.clip(upper=0)
    roll_up = up.ewm(alpha=1 / period, adjust=False).mean()
    roll_down = down.ewm(alpha=1 / period, adjust=False).mean()
    rs = roll_up / roll_down.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])


def ma(series: pd.Series, window: int) -> float:
    return float(series.rolling(window).mean().iloc[-1])


def realized_vol(series: pd.Series, window: int = 30) -> float:
    rets = np.log(series / series.shift(1)).dropna()
    vol = rets.tail(window).std() * np.sqrt(365)  # годовая
    return float(vol)


def max_drawdown(series: pd.Series, window: int = 30) -> float:
    s = series.tail(window)
    cummax = s.cummax()
    dd = (s - cummax) / cummax
    return float(dd.min())  # отрицательное число

