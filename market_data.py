#%%
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta
import os, sys
import ta
import time

from safe_download import cache_path, load_cache, save_cache, save_snapshot


def get_data(ticker, days, intvl, force_refresh=False):
    path = cache_path(ticker, days, intvl, prepost=True)
    
    if not force_refresh:
        data = load_cache(path, max_age_minutes=60, allow_stale=False)
        if data is not None and not data.empty:
            print(f"loaded {ticker} from cache: {path}")
            return data
    
    tries, pause = 7, 60. # 3 attempts, 20s apart
    last_err = None
    data = pd.DataFrame()
    for attempt in range(1, tries + 1):
        try:
            data = yf.download(
                ticker, 
                period = days, 
                interval = intvl, 
                prepost = True,
                progress=False,
                auto_adjust=False,
            )
            if not data.empty:
                break      
        except Exception as e:
            print(f"download attempt {attempt} failed for {ticker}: {e}")
            last_err = e
        if attempt < tries:
             print(f"attempt {attempt}/{tries} failed or empty. Retrying in {pause}s...")
             time.sleep(pause) 

    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if data.index.tz is not None:
            data = data.tz_convert("US/Eastern")
        save_cache(data, path)
        save_snapshot(data, ticker, days, intvl, True)
        return data
    
    stale = load_cache(path, allow_stale=True)
    if stale is not None and not stale.empty:
        print(f"using stale cache for {ticker}: {path}")
        return stale
    
    if last_err:
        print(f"all download attempts failed for {ticker}: {last_err}")
    return pd.DataFrame()
    
    
def add_rsi(data, rsi_window, col="Close"):
    if data.empty or len(data) < rsi_window + 1:
            return data.assign(**{f"RSI{rsi_window}": pd.Series([pd.NA]*len(data), index=data.index)})
       
    s = data[col]
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    s = s.squeeze()
    rsi = ta.momentum.RSIIndicator(close=s, window=rsi_window).rsi()
    out = data.assign(**{f"RSI{rsi_window}": rsi})
    return out
    

#%%