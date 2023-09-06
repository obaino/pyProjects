#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# doesn't include the change

# https://pypi.org/project/yfinance/
# https://pypi.org/project/tabulate/

import yfinance as yf
from tabulate import tabulate

def main():
    gold_price = get_gold_price()
    gs_price = get_GoldmanSachs_price()
    pm_price = get_Pimco_price()
    sc_price = get_Schroder_price()
    lgt_price = get_LGT_price()

    d = {
        "Gold": gold_price,
        "Goldman Sachs Liquid Reserves Fund": gs_price,
        "PIMCO GIS Income Fund": pm_price,
        "Schroder International Selection Fund": sc_price,
        "LGT GIM Balanced": lgt_price,
        }
    
    headers = ["Asset", "Price"]

    print(tabulate([(k,) + v for k, v in d.items()], headers=headers, tablefmt="grid"))


def get_gold_price():
    # Create a Ticker object for gold (symbol: "GC=F")
    gold_ticker = yf.Ticker("GC=F")

    # Fetch historical data (2 day) to get the latest price
    historical_data = gold_ticker.history(period="3d")

    # Get the latest gold price (Close price of the most recent day)
    # pre_latest_gold_price = historical_data["Close"].iloc[-2]
    latest_gold_price = historical_data["Close"].iloc[-1]
    # output = (latest_gold_price - pre_latest_gold_price) / pre_latest_gold_price * 100

    return latest_gold_price

def get_GoldmanSachs_price():
    # Goldman Sachs US$ Liquid Reserves Fund
    # https://finance.yahoo.com/quote/0P00000TMT
    # ISIN: IE0031294410
    # pcs, price = (4.6080, 11945.2387
    # )
    ticker = yf.Ticker("0P00000TMT")

    historical_data = ticker.history(period="3d")

    # pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    # output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price

def get_Pimco_price():
    # PIMCO GIS plc - Income Fund (0P0000X83M)
    # https://finance.yahoo.com/quote/0P0000X83M
    # ISIN: 
    # pcs, price = (1,015.69700, $10.83)

    ticker = yf.Ticker("0P0000X83M")

    historical_data = ticker.history(period="3d")

    # pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    # output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price

def get_Schroder_price():
    # Schroder International Selection Fund Global Credit
    # https://finance.yahoo.com/quote/0P00019BR5
    # ISIN: 
    # pcs, price = (100.58000, $102.426)

    ticker = yf.Ticker("0P00019BR5")

    historical_data = ticker.history(period="3d")

    # pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    # output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price

def get_LGT_price():
    # LGT Multi-Assets SICAV - LGT GIM Balanced
    # https://finance.yahoo.com/quote/0P0000ND55
    # ISIN: LI0108468880
    # pcs, price = (76, 12647.7436)

    ticker = yf.Ticker("0P0000ND55")

    historical_data = ticker.history(period="1mo")

    # pre_latest_price = historical_data["Close"].iloc[-2]
    latest_price = historical_data["Close"].iloc[-1]
    # output = (latest_price - pre_latest_price) / pre_latest_price * 100

    return latest_price

if __name__ == "__main__":
    main()