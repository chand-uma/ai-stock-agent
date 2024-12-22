import pandas as pd
import numpy as np
import logging

def prepare_features(data):
    """
    Perform feature engineering on the stock data.
    """
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['Volume_Change'] = data['Volume'].pct_change()
    data = data.dropna()
    if data.empty:
        logging.error("Insufficient data after feature engineering. Exiting.")
        return None, None
    features = data[['SMA_10', 'SMA_50', 'Volume_Change']]
    labels = data['Direction']
    return features, labels