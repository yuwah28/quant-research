import os
import time
import pandas as pd

CACHE_DIR = "data/processed"
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_path(tick, period, interval, prepost):
    stamp = f"{tick}_{period}_{interval}_{'pre' if prepost else 'reg'}.csv"
    return os.path.join(CACHE_DIR, stamp)

def load_cache(path, max_age_minutes=60):
    if not os.path.exists(path):
        return None
    mtime = os.path.getmtime(path)
    if (time.time() - mtime) > max_age_minutes * 60:
        return None
    try:
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        return df
    except Exception:
        return None

def save_cache(df, path):
    
    try:
        df.to_csv(path)
    except Exception:
        pass
