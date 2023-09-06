#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://pypi.org/project/yfinance/
import yfinance as yf
from tabulate import tabulate

def main():
    gold_price, gold_change = get_gold_price()
    gs_price, gs_change = get_GoldmanSachs_price()
    pm_price, pm_change = get_Pimco_price()
    sc_price, sc_change = get_Schroder_price()
    lgt_price = get_LGT_price()

    d = {
        "Gold": (gold_price, gold_change),
        "Goldman Sachs Liquid Reserves Fund": (gs_price, gs_change),
        "PIMCO GIS Income Fund": (pm_price, pm_change),
        "Schroder International Selection Fund": (sc_price, sc_change),
        "LGT GIM Balanced": (lgt_price, None)
        }
    
    headers = ["Asset", "Price", "Change"]

    print(tabulate([(k,) + v for k, v in d.items()], headers=headers, tablefmt="grid"))

    # print(f"Gold Price is: ${gold_price:.2f} changing at {gold_change:.2f}%")
    # print("----" * 16)
    # print(f"Goldman Sachs Liquid Reserves Fund is: ${gs_price:.2f} changing at {gs_change:.2f}%")
    # print("----" * 16)
    # print(f"PIMCO GIS Income Fund is: ${pm_price:.2f} changing at {pm_change:.2f}%")
    # print("----" * 16)
    # print(f"Schroder International Selection Fund is: ${sc_price:.2f} changing at {sc_change:.2f}%")

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
    # Goldman Sachs US$ Liquid Reserves Fund
    # https://finance.yahoo.com/quote/0P00000TMT
    # ISIN: IE0031294410
    # pcs, price = (4.6080, 11945.2387
    # )
    ticker = yf.Ticker("0P00000TMT")

    historical_data = ticker.history(period="3d")

    pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price, output

def get_Pimco_price():
    # PIMCO GIS plc - Income Fund (0P0000X83M)
    # https://finance.yahoo.com/quote/0P0000X83M
    # ISIN: 
    # pcs, price = (1,015.69700, $10.83)

    ticker = yf.Ticker("0P0000X83M")

    historical_data = ticker.history(period="3d")

    pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price, output

def get_Schroder_price():
    # Schroder International Selection Fund Global Credit
    # https://finance.yahoo.com/quote/0P00019BR5
    # ISIN: 
    # pcs, price = (100.58000, $102.426)

    ticker = yf.Ticker("0P00019BR5")

    historical_data = ticker.history(period="3d")

    pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price, output

def get_LGT_price():
    # LGT Multi-Assets SICAV - LGT GIM Balanced
    # https://finance.yahoo.com/quote/0P0000ND55
    # ISIN: LI0108468880
    # pcs, price = (76, 12647.7436)

    ticker = yf.Ticker("0P0000ND55")

    historical_data = ticker.history(period="3d")

    # pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    # output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price

if __name__ == "__main__":
    main()