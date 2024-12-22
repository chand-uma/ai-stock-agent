import logging

def execute_trades(data, ticker, api):
    """
    Execute trades based on the generated signals.
    """
    for index, row in data.iterrows():
        if row['Signal'] == 1:  # Buy Signal
            logging.info(f"Buying {ticker} at {row['Close']} on {index}")
        elif row['Signal'] == 0 and position_qty > 0:  # Sell Signal
            try:
                api.submit_order(
                    symbol=ticker,
                    qty=position_qty,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                logging.info(f"Sold {position_qty} shares of {ticker} at {row['Close']}")
            except Exception as e:
                logging.error(f"Error executing sell order for {ticker}: {e}")