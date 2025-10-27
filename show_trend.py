#%%
from market_data import get_data, add_rsi
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

from IPython.display import display

# Default parameters
ticker = "GOOG"
days, intvl = "5d", "15m"
rsi_window = 14
line_type_default = "line"


def fetch_trend(ticker=ticker, days=days, intvl=intvl, line_type=line_type_default, rsi_window=rsi_window, out_dir="plots"):
    data = get_data(ticker, days, intvl)
    data = add_rsi(data, rsi_window=rsi_window, col="Close")

    rsi_col = f"RSI{rsi_window}"
    if data.empty or rsi_col not in data.columns:
        print(f"No data or {rsi_col} to plot for {ticker}")
        return None
    
    print(data[[rsi_col]].tail())

    rsi_series = data[rsi_col].dropna()
    if rsi_series.empty:
        print(f"{rsi_col} is all NaN; not plotting RSI.")
        return None
    
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{ticker}_{days}_{intvl}.png")

    ap = [mpf.make_addplot(data[rsi_col], panel=2, ylabel=rsi_col)]
    style = mpf.make_mpf_style(base_mpf_style="yahoo", gridstyle=":", y_on_right=False)
    fig, _ = mpf.plot(
        data,
        type=line_type,
        volume=True,
        addplot=ap,
        panel_ratios=(3, 1, 1),
        title=f"{ticker} — {days} ({intvl}, pre/post)",
        style=style,
        returnfig=True, 
        savefig=path,
        closefig=False,
    )
    display(fig)
     
    print(f"Saved chart → {path}")
    return path

#%%