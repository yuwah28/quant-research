# SConstruct
import os, sys
from SCons.Script import Environment, ARGUMENTS, Default

sys.path.insert(0, os.getcwd())

from show_trend import fetch_trend

env = Environment(ENV=os.environ)


TICKER = ARGUMENTS.get('TICKER', 'LUNR')
DAYS   = ARGUMENTS.get('DAYS',   '5d')
INTVL  = ARGUMENTS.get('INTVL',  '15m')
RSI    = int(ARGUMENTS.get('RSI','14'))
STYLE  = ARGUMENTS.get('STYLE',  'candle')   # or 'line'


target_png = f"plots/{TICKER}_{DAYS}_{INTVL}.png"

def build_plot(target, source, env):
    out = fetch_trend(
        ticker=TICKER, days=DAYS, intvl=INTVL,
        rsi_window=RSI, line_type=STYLE, out_dir='plots'
    )
    if out is None or not os.path.exists(out):
        return 1
    return None

env.Command(target=target_png, source=[], action=build_plot)
Default(target_png)
