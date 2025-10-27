#%%
from market_data import get_data, add_rsi
import mplfinance as mpf
import os

# Default parameters
ticker = "GOOG"
days, intvl = "5d", "15m"
rsi_window = 14

def fetch_trend(ticker=ticker, days=days, intvl=intvl, rsi_window=rsi_window, out_dir="plots"):
    data = get_data(ticker, days, intvl)
    data = add_rsi(data, rsi_window=rsi_window, col="Close")

    rsi_col = f"RSI{rsi_window}"
    if data.empty or rsi_col not in data.columns:
        print(f"No data or {rsi_col} to plot for {ticker}")
        return None
    
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{ticker}_{days}_{intvl}.png")

    ap = [mpf.make_addplot(data[rsi_col], panel=1, ylabel=rsi_col)]
    style = mpf.make_mpf_style(base_mpf_style="yahoo", gridstyle=":", y_on_right=False)
    mpf.plot(
        data,
        type="candle",
        volume=True,
        addplot=ap,
        panel_ratios=(3, 1),
        title=f"{ticker} — {days} ({intvl}, pre/post)",
        style=style,
        savefig=path,
    )

    print(f"Saved chart → {path}")
    return path

#%%