# created by gemini to calculate the exact historical portfolio value at each deposit date,
# accounting for all trades and cash flows up to that point.
# This allows you to determine the precise pre-deposit portfolio value for accurate IRR calculations.

import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Dynamically read external data sources using Pandas
try:
    df_cash_flows = pd.read_csv('cash_flows.csv')
    df_trades = pd.read_csv('trades.csv')
except FileNotFoundError as e:
    print(f"Error: Could not find data files. Make sure 'cash_flows.csv' and 'trades.csv' are in the same folder. Detailed error: {e}")
    exit()

# Convert dataframes back to lists of dictionaries for your calculation logic
cash_flows = df_cash_flows.to_dict(orient='records')
trades = df_trades.to_dict(orient='records')

# Tickers map
tickers = {'VAGF': 'VAGF.DE', 'VWCE': 'VWCE.DE', 'VWRA': 'VWRA.L'}

def get_hist_price(ticker, date_str):
    """Fetches the nearest available market closing price on or before the date."""
    data = yf.download(ticker, end=date_str, progress=False)
    if data.empty:
        start_dt = pd.to_datetime(date_str) - pd.Timedelta(days=7)
        data = yf.download(ticker, start=start_dt.strftime('%Y-%m-%d'), end=date_str, progress=False)
        
    if not data.empty:
        last_close = data['Close'].iloc[-1]
        if hasattr(last_close, 'squeeze'):
            last_close = last_close.squeeze()
        return float(last_close)
    return 0.0

print(f"{'Date':<12} | {'Cash Input':<12} | {'Exact Pre-Deposit Portfolio Value (EUR)':<40}")
print("-" * 75)

# Tracking states
shares_owned = {'VAGF': 0.0, 'VWCE': 0.0, 'VWRA': 0.0}
running_eur_cash = 0.0
running_usd_cash = 0.0

# Combine deposits and trades chronologically
all_events = []
for cf in cash_flows:
    all_events.append({"date": cf["date"], "type": "deposit", "data": cf})
for t in trades:
    all_events.append({"date": t["date"], "type": "trade", "data": t})

all_events = sorted(all_events, key=lambda x: (x["date"], x["type"] == "trade"))

for event in all_events:
    date_str = event["date"]
    
    if event["type"] == "deposit":
        v_vagf = shares_owned['VAGF'] * get_hist_price(tickers['VAGF'], date_str)
        v_vwce = shares_owned['VWCE'] * get_hist_price(tickers['VWCE'], date_str)
        
        p_vwra_usd = get_hist_price(tickers['VWRA'], date_str)
        fx_usd_eur = get_hist_price('USDEUR=X', date_str)
        v_vwra_eur = (shares_owned['VWRA'] * p_vwra_usd) * fx_usd_eur
        
        total_value_eur = v_vagf + v_vwce + v_vwra_eur + running_eur_cash + (running_usd_cash * fx_usd_eur)
        
        # Access dictionary values using CSV header keys
        print(f"{date_str:<12} | €{event['data']['amount_eur']:<10,.2f} | €{total_value_eur:<38,.2f}")
        
        amount = event['data']['amount_eur']
        if date_str in ["2024-08-11", "2024-08-16", "2025-02-14", "2026-06-03"]:
            running_usd_cash += amount / fx_usd_eur
        else:
            running_eur_cash += amount
        
    elif event["type"] == "trade":
        t_data = event["data"]
        shares_owned[t_data['etf']] += t_data['shares']
        running_eur_cash += t_data['cash_impact_eur']
        running_usd_cash += t_data['cash_impact_usd']