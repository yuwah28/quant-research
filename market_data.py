#%%
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import ta
from datetime import datetime, timedelta


def get_data(ticker, days, intvl):
    data = yf.download(
        ticker, 
        period = days, 
        interval = intvl, 
        prepost = True,
        auto_adjust = False)
    return data


ticker = "QUBT"
days, intvl = "5d", "15m"
data = get_data(ticker, days, intvl)

print(data.head())

plt.figure(figsize=(10 , 5))
plt.plot(data.index, data['Close'], label=f'{ticker} Close Price')
plt.title(f'{ticker} Stock Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid()
plt.show()

#%%