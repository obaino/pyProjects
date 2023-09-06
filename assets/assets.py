#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://pypi.org/project/yfinance/
import yfinance as yf

def main():
    gold_price, day_difference = get_gold_price()
    gs_price, gs_day_difference = get_GoldmanSachs_price()

    print(f"Goldman Sachs Liquid Reserves Fund is: ${gs_price:.2f} changing at {gs_day_difference:.2f}%")
    print(f"Gold Price is: ${gold_price:.2f} changing at {day_difference:.2f}%")

def get_gold_price():
    # Create a Ticker object for gold (symbol: "GC=F")
    gold_ticker = yf.Ticker("GC=F")

    # Fetch historical data (2 day) to get the latest price
    historical_data = gold_ticker.history(period="3d")

    # Get the latest gold price (Close price of the most recent day)
    pre_latest_gold_price = historical_data["Close"].iloc[-2]
    latest_gold_price = historical_data["Close"].iloc[-1]
    output = (latest_gold_price - pre_latest_gold_price) / pre_latest_gold_price * 100

    return latest_gold_price, output

def get_GoldmanSachs_price():
    gs_ticker = yf.Ticker("0P00000TMT")

    historical_data = gs_ticker.history(period="3d")

    pre_latest_gs_price = historical_data["Close"].iloc[-2]
    latest_gs_price = historical_data["Close"].iloc[-1]
    output = (latest_gs_price - pre_latest_gs_price) / pre_latest_gs_price * 100

    return latest_gs_price, output

if __name__ == "__main__":
    main()