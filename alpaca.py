from alpaca_trade_api.rest import REST

api = REST('API_KEY', 'SECRET_KEY', base_url='https://paper-api.alpaca.markets')
data = api.get_barset(['AAPL'], 'minute', limit=100).df
print(data)
