#%%

import os
import time
import pandas as pd
from datetime import datetime

CACHE_DIR = "data/processed"
SNAP_DIR  = "data/snapshots"      
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(SNAP_DIR, exist_ok=True) 

def cache_path(tick, period, interval, prepost):
    stamp = f"{tick}_{period}_{interval}_{'pre' if prepost else 'reg'}.csv"
    return os.path.join(CACHE_DIR, stamp)

def load_cache(path, max_age_minutes=60, allow_stale=False):
    if not os.path.exists(path):
        return None
    if not allow_stale:
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
    
def snapshot_path(tick, period, interval, prepost):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{tick}_{period}_{interval}_{'pre' if prepost else 'reg'}_{ts}.parquet"
    return os.path.join(SNAP_DIR, name)

def save_snapshot(df, tick, period, interval, prepost):
    try:
        df.to_parquet(snapshot_path(tick, period, interval, prepost))
    except Exception:
        pass
#%%