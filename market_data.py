#%%
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import ta
from datetime import datetime, timedelta


def get_data(ticker, days, intvl):
    # grep ticker data
    data = yf.download(
        ticker, 
        period = days, 
        interval = intvl, 
        prepost = True,
        auto_adjust = False,
        progress=False,
    )
    
    if data.index.tz is not None:
        data = data.tz_convert("US/Eastern")
    return data
    
def add_rsi(data, rsi_window=14, col="Close"):
    out = data.copy()
    out[f"RSI{rsi_window}"] = ta.momentum.RSIIndicator(
        close=out[col], window=rsi_window
    ).rsi()
    return out
    


ticker = "QUBT"
days, intvl = "5d", "15m"
data = get_data(ticker, days, intvl)
data = add_rsi(data, rsi_window=14, col="Close")



# build the RSI addplot (separate panel)
ap = [
    mpf.make_addplot(
        data["RSI14"], panel=1, ylabel="RSI(14)"
    )
]

style = mpf.make_mpf_style(base_mpf_style="yahoo", gridstyle=":", y_on_right=False)

mpf.plot(
    data,
    type="candle",
    volume=True,
    addplot=ap,
    panel_ratios=(3, 1),
    title=f"{ticker} — {days} ({intvl}, pre/post)",
    style=style,
)
#%%