#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
assets.py — Personal investment price tracker
Fetches latest prices and day-over-day change for a mixed portfolio
of ETFs, futures, and mutual funds via yfinance.
"""

import yfinance as yf
from tabulate import tabulate
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION — edit only this section
# ─────────────────────────────────────────────
ASSETS = [
    # (Display name,                            Ticker,       Category)
    ("Gold Futures",                            "GC=F",       "commodity"),
    ("VWRA – Vanguard All-World (USD, LSE)",    "VWRA.L",     "etf"),
    ("VWCE – Vanguard All-World (EUR, XETRA)",  "VWCE.DE",    "etf"),
    ("VAGF – Vanguard Global Aggregate Bond (EUR, LSE)", "VAGF.DE", "etf"),
    ("PIMCO GIS Income Fund",                   "0P0000X83M", "fund"),
    ("Schroder Intl Selection Fund",            "0P00019BR5", "fund"),
    ("LGT GIM Balanced",                        "0P0000ND55", "fund"),
]

# How many past trading sessions to fetch (keeps it minimal)
HISTORY_PERIOD = "5d"  # 5 days = always enough for 2 valid sessions
# ─────────────────────────────────────────────


def fetch_asset(name: str, ticker: str) -> dict:
    """Fetch latest price and % change for a single asset."""
    data = yf.Ticker(ticker).history(period=HISTORY_PERIOD, auto_adjust=True)

    if data.empty or len(data) < 1:
        return {"name": name, "ticker": ticker, "price": None,
                "change": None, "date": None, "error": "No data returned"}

    # Drop any rows where Close is NaN (can happen with infrequent funds)
    closes = data["Close"].dropna()

    latest_price = closes.iloc[-1]
    latest_date  = closes.index[-1].strftime("%Y-%m-%d")

    if len(closes) >= 2:
        prev_price = closes.iloc[-2]
        change_pct = (latest_price - prev_price) / prev_price * 100
    else:
        change_pct = None  # Only one session available (e.g. fund updated weekly)

    return {
        "name":   name,
        "ticker": ticker,
        "price":  latest_price,
        "change": change_pct,
        "date":   latest_date,
        "error":  None,
    }


def format_change(change) -> str:
    if change is None:
        return "N/A"
    arrow = "▲" if change >= 0 else "▼"
    color = ""  # extend with colorama later if you want color in terminal
    return f"{arrow} {change:+.2f}%"


def build_table(results: list) -> list:
    rows = []
    for r in results:
        if r["error"]:
            rows.append([r["name"], r["ticker"], "—", r["error"], "—"])
        else:
            rows.append([
                r["name"],
                r["ticker"],
                f"{r['price']:.4f}",
                format_change(r["change"]),
                r["date"],
            ])
    return rows


def main():
    print(f"\n📊 Portfolio Prices — {datetime.now().strftime('%A %d %b %Y, %H:%M')}\n")

    results = []
    for name, ticker, category in ASSETS:
        result = fetch_asset(name, ticker)
        result["category"] = category
        results.append(result)

    headers = ["Asset", "Ticker", "Price", "Change", "Last Update"]
    table   = build_table(results)

    print(tabulate(table, headers=headers, tablefmt="rounded_outline",
                   colalign=("left", "left", "right", "right", "center")))
    print()


if __name__ == "__main__":
    main()
