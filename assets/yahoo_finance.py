#!/usr/bin/env python3
# VWRA.L VWCE.DE

import yfinance as yf
import argparse
from tabulate import tabulate

def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data.append([
            ticker,
            info['regularMarketPrice'],
            info['regularMarketChange'],
            info['regularMarketChangePercent'],
            info['regularMarketVolume']
        ])
    return data

def main():
    parser = argparse.ArgumentParser(description='Display Yahoo Finance data')
    parser.add_argument('tickers', nargs='+', help='Stock tickers to display')
    args = parser.parse_args()

    data = get_stock_data(args.tickers)
    headers = ['Ticker', 'Price', 'Change', 'Change %', 'Volume']
    print(tabulate(data, headers=headers, floatfmt='.2f'))

if __name__ == '__main__':
    main()
