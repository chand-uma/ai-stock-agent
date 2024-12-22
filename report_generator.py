import logging

def generate_daily_report(data):
    """
    Generate a daily trading report.
    """
    if data.empty:
        logging.error("Data is empty. Cannot generate report.")
        return "No data available to generate report."

    profit_loss = data['Close'].iloc[-1] - data['Close'].iloc[0]
    tickers = ', '.join(data['Ticker'].unique().astype(str))
    report = f"Daily Trading Report:\nTickers: {tickers}\nProfit/Loss: {profit_loss:.2f}\n"
    return report