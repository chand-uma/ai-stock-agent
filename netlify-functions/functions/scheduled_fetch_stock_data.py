import json
import yfinance as yf

def handler(event, context):
    ticker = 'AAPL'  # You can change this to any ticker you want to fetch
    data = yf.download(ticker, period="1d", interval="1m")
    data_json = data.to_json(orient='records')
    return {
        'statusCode': 200,
        'body': data_json,
        'headers': {
            'Content-Type': 'application/json'
        }
    }