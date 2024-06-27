#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_and_save_data(ticker, filename):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="1m")
    hist.to_csv(filename)

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"] 

    for ticker in tickers:
        filename = f"{ticker}_{datetime.today().strftime('%Y-%m-%d')}.csv"
        fetch_and_save_data(ticker, filename)

