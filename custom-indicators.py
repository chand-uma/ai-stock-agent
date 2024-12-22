def compute_indicators(data):
    data['SMA_50'] = data['Adj Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Adj Close'].rolling(window=200).mean()
    data['RSI'] = compute_rsi(data['Adj Close'], 14)
    return data

data = compute_indicators(data)
