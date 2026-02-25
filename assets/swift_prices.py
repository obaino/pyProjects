#!/Users/nikolask/Myfiles/gitPython/.gitPython-venv/bin/python3
# -*- coding: utf-8 -*-

import yfinance as yf

# Customize your watchlist here
SYMBOLS = {
    "GC=F":     "Gold",
    "VAGF.DE":      "VAGF",
    "VWRA.L":      "VWRA",
    "VWCE.DE":  "VWCE",
}

def format_line(label, price, change_pct):
    arrow = "▲" if change_pct >= 0 else "▼"
    color = "green" if change_pct >= 0 else "red"
    return f"{label}: {price:.2f} {arrow}{abs(change_pct):.1f}% | color={color}"

results = []
for symbol, label in SYMBOLS.items():
    try:
        info = yf.Ticker(symbol).fast_info
        price = info.last_price
        prev  = info.previous_close
        pct   = ((price - prev) / prev) * 100
        results.append(format_line(label, price, pct))
    except Exception as e:
        results.append(f"{label}: N/A | color=gray")

# First line appears in the menu bar itself
print(results[0])
print("---")
for line in results[1:]:
    print(line)
