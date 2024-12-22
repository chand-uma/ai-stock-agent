import yfinance as yf
import pandas as pd
import logging

def fetch_data(ticker):
    """
    Fetch real-time data for a stock ticker using yfinance.
    """
    data = yf.download(ticker, period="1d", interval="1m")
    if not data.empty:
        data['Ticker'] = ticker
    return data