import requests
import pandas as pd
import logging
import os
from dotenv import load_dotenv
from feature_engineering import prepare_features
from trade_executor import execute_trades
from report_generator import generate_daily_report
from notifier import send_sms_report, send_email_report

# Load environment variables from a .env file
load_dotenv()

def fetch_data(ticker):
    """
    Fetch real-time data for a stock ticker using Netlify Function.
    """
    url = f"https://ai-stock-agent.netlify.app/.netlify/functions/fetch_stock_data?ticker={ticker}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['Ticker'] = ticker
    return df

# Main Function
def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL']  # Example tickers
    all_data = pd.DataFrame()

    for ticker in tickers:
        data = fetch_data(ticker)
        if data is None or data.empty:
            logging.warning(f"No data fetched for {ticker}. Skipping.")
            continue
        all_data = pd.concat([all_data, data])

    report = generate_daily_report(all_data)
    print(report)
    #send_sms_report(report)
    #send_email_report("Daily Trading Report", report, "recipient@example.com")

if __name__ == "__main__":
    main()