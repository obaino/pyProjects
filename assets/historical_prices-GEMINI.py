# created by gemini to calculate the exact historical portfolio value at each deposit date,
# accounting for all trades and cash flows up to that point.
# This allows you to determine the precise pre-deposit portfolio value for accurate IRR calculations.

import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Your exact historical deposit timeline (from Cash_Flows tab)
cash_flows = [
    {"date": "2024-08-11", "amount_eur": 6413.89},
    {"date": "2024-08-16", "amount_eur": 6342.70},
    {"date": "2025-02-02", "amount_eur": 6000.00},
    {"date": "2025-02-09", "amount_eur": 6000.00},
    {"date": "2025-02-11", "amount_eur": 6000.00},
    {"date": "2025-02-14", "amount_eur": 8563.93},
    {"date": "2025-02-17", "amount_eur": 10000.00},
    {"date": "2025-02-25", "amount_eur": 10000.00},
    {"date": "2025-11-25", "amount_eur": 5000.00},
    {"date": "2025-12-01", "amount_eur": 5000.00},
    {"date": "2026-05-20", "amount_eur": 5000.00},
    {"date": "2026-05-22", "amount_eur": 5000.00},
    {"date": "2026-06-02", "amount_eur": 5000.00},
    {"date": "2026-06-03", "amount_eur": 41746.67},
    {"date": "2026-07-01", "amount_eur": 5000.00},
    {"date": "2026-07-02", "amount_eur": 1822.70}   # today's deposit
]

# 2. Your complete trading ledger (from Trades tab + today's trade)
trades = [
    {"date": "2024-08-15", "etf": "VWRA", "shares": 52, "cash_impact_usd": -6873.20, "cash_impact_eur": 0},
    {"date": "2024-09-11", "etf": "VWRA", "shares": 25, "cash_impact_usd": -3291.50, "cash_impact_eur": 0},
    {"date": "2025-01-08", "etf": "VWRA", "shares": 23, "cash_impact_usd": -3190.42, "cash_impact_eur": 0},
    {"date": "2025-02-11", "etf": "VWCE", "shares": 85, "cash_impact_usd": 0, "cash_impact_eur": -11820.91},
    {"date": "2025-02-12", "etf": "VWCE", "shares": 30, "cash_impact_usd": 0, "cash_impact_eur": -4149.00},
    {"date": "2025-02-20", "etf": "VWCE", "shares": 45, "cash_impact_usd": 0, "cash_impact_eur": -6250.02},
    {"date": "2025-02-24", "etf": "VWCE", "shares": 40, "cash_impact_usd": 0, "cash_impact_eur": -5499.00},
    {"date": "2025-02-24", "etf": "VWRA", "shares": 35, "cash_impact_usd": -5015.30, "cash_impact_eur": 0},
    {"date": "2025-02-27", "etf": "VWRA", "shares": 30, "cash_impact_usd": -4282.00, "cash_impact_eur": 0},
    {"date": "2025-03-03", "etf": "VWCE", "shares": 40, "cash_impact_usd": 0, "cash_impact_eur": -5460.60},
    {"date": "2025-03-04", "etf": "VWCE", "shares": 30, "cash_impact_usd": 0, "cash_impact_eur": -3954.00},
    {"date": "2025-11-27", "etf": "VAGF", "shares": 230, "cash_impact_usd": 0, "cash_impact_eur": -5497.70},
    {"date": "2025-12-04", "etf": "VAGF", "shares": 220, "cash_impact_usd": 0, "cash_impact_eur": -5239.00},
    {"date": "2026-05-21", "etf": "VAGF", "shares": 63.8297, "cash_impact_usd": 0, "cash_impact_eur": -1503.00},
    {"date": "2026-05-22", "etf": "VWCE", "shares": 20, "cash_impact_usd": 0, "cash_impact_eur": -3221.00},
    {"date": "2026-05-25", "etf": "VAGF", "shares": 64.17, "cash_impact_usd": 0, "cash_impact_eur": -1521.26},
    {"date": "2026-05-25", "etf": "VWCE", "shares": 22, "cash_impact_usd": 0, "cash_impact_eur": -3579.76},
    {"date": "2026-06-02", "etf": "VAGF", "shares": 150, "cash_impact_usd": 0, "cash_impact_eur": -3565.93},
    {"date": "2026-06-02", "etf": "VWCE", "shares": 9, "cash_impact_usd": 0, "cash_impact_eur": -1477.33},
    {"date": "2026-06-03", "etf": "VWRA", "shares": 45, "cash_impact_usd": -8566.96, "cash_impact_eur": 0},
    {"date": "2026-06-05", "etf": "VWRA", "shares": 45, "cash_impact_usd": -8500.33, "cash_impact_eur": 0},
    {"date": "2026-07-06", "etf": "VWRA", "shares": 45, "cash_impact_usd": -8539.04, "cash_impact_eur": 0} # Today's purchase
]

# Tickers map
tickers = {'VAGF': 'VAGF.DE', 'VWCE': 'VWCE.DE', 'VWRA': 'VWRA.L'}

def get_hist_price(ticker, date_str):
    """Fetches the nearest available market closing price on or before the date.
    Falls back gracefully to wider intervals if weekends/holidays return empty data.
    """
    # 1. Try the standard download up to the target date
    data = yf.download(ticker, end=date_str, progress=False)
    
    # 2. If it's empty (e.g., weekend/holiday API anomalies), expand search window backward
    if data.empty:
        # Fetch a 7-day historical window surrounding the date to catch the closest market close
        start_dt = pd.to_datetime(date_str) - pd.Timedelta(days=7)
        data = yf.download(ticker, start=start_dt.strftime('%Y-%m-%d'), end=date_str, progress=False)
        
    if not data.empty:
        last_close = data['Close'].iloc[-1]
        if hasattr(last_close, 'squeeze'):
            last_close = last_close.squeeze()
        return float(last_close)
        
    return 0.0

# def get_hist_price(ticker, date_str):
#     """Fetches the nearest available market closing price on or before the date"""
#     data = yf.download(ticker, end=date_str, progress=False)
#     if not data.empty:
#         last_close = data['Close'].iloc[-1]
#         if hasattr(last_close, 'squeeze'):
#             last_close = last_close.squeeze()
#         return float(last_close)
#     return 0.0

print(f"{'Date':<12} | {'Cash Input':<12} | {'Exact Pre-Deposit Portfolio Value (EUR)':<40}")
print("-" * 75)

# Keep track of running share count totals and cash segments
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
        # Calculate asset valuation right before this deposit alters the balance
        v_vagf = shares_owned['VAGF'] * get_hist_price(tickers['VAGF'], date_str)
        v_vwce = shares_owned['VWCE'] * get_hist_price(tickers['VWCE'], date_str)
        
        # VWRA is priced in USD on LSE, fetch USD close and convert to EUR using USDEUR=X
        p_vwra_usd = get_hist_price(tickers['VWRA'], date_str)
        fx_usd_eur = get_hist_price('USDEUR=X', date_str)
        v_vwra_eur = (shares_owned['VWRA'] * p_vwra_usd) * fx_usd_eur
        
        # Total portfolio value = Asset values + Cash reserves currently sitting in account
        total_value_eur = v_vagf + v_vwce + v_vwra_eur + running_eur_cash + (running_usd_cash * fx_usd_eur)
        
        print(f"{date_str:<12} | €{event['data']['amount_eur']:<10,.2f} | €{total_value_eur:<38,.2f}")
        
        # Cleanly route deposits into their actual operational currencies
        amount = event['data']['amount_eur']
        
        # Route specific deposits to USD track via the live conversion rate
        if date_str in ["2024-08-11", "2024-08-16", "2025-02-14", "2026-06-03"]:
            running_usd_cash += amount / fx_usd_eur
        else:
            running_eur_cash += amount
        
    elif event["type"] == "trade":
        t_data = event["data"]
        shares_owned[t_data['etf']] += t_data['shares']
        running_eur_cash += t_data['cash_impact_eur']
        running_usd_cash += t_data['cash_impact_usd']