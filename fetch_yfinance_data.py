import yfinance as yf

# Fetch real-time data for a stock
ticker = 'AAPL'
data = yf.download(ticker, period="1d", interval="1m")
print(data.tail())
