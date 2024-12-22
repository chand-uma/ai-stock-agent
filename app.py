import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import logging
from datetime import datetime
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Alpaca API Credentials
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets/v2'

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')

FROM_EMAIL = os.getenv('FROM_EMAIL')
FROM_PASSWORD = os.getenv('FROM_PASSWORD')

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Check Alpaca API installation
try:
    from alpaca_trade_api.rest import REST, TimeFrame
    api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=BASE_URL)
except ModuleNotFoundError:
    logging.error("alpaca_trade_api module not found. Install it using 'pip install alpaca-trade-api'.")
    api = None

# Fetch Historical Data
# Fetch Historical Data
def fetch_data(ticker, period='1y', interval='1d'):
    logging.info(f"Fetching data for {ticker}")
    data = yf.download(ticker, period=period, interval=interval)
    if data.empty:
        logging.error(f"No data retrieved for ticker {ticker}. Exiting.")
        return None
    data['Return'] = data['Close'].pct_change()
    data['Direction'] = np.where(data['Return'] > 0, 1, 0)
    data = data.dropna()
    data['Ticker'] = ticker  # Add the ticker symbol as a column
    return data

# Feature Engineering
def prepare_features(data):
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

# Train Model
def train_model(features, labels):
    if features is None or labels is None:
        logging.error("No features or labels available for training. Exiting.")
        return None
    logging.info("Training model")
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    logging.info(f"Model accuracy: {accuracy:.2f}")
    return model

# Generate Signals
def generate_signals(model, data):
    if model is None or data.empty:
        logging.error("No model or data available for generating signals. Exiting.")
        return data
    logging.info("Generating trade signals")
    features, _ = prepare_features(data)
    if features is None:
        logging.error("No features available for generating signals. Exiting.")
        return data
    data['Signal'] = model.predict(features)
    return data

# Check Pattern Day Trading Rule
def check_pattern_day_trading():
    try:
        account = api.get_account()
        if float(account.equity) < 25000:
            logging.warning("Pattern Day Trading rule applies. Restricting trades to 3 per 5 trading days.")
            return False
    except Exception as e:
        logging.error(f"Error checking pattern day trading rule: {e}")
    return True

# Execute Trades
def execute_trades(data, tickers):
    if api is None:
        logging.error("Alpaca API is not initialized. Cannot execute trades.")
        return

    if data.empty:
        logging.error("No data available for executing trades. Exiting.")
        return

    if not check_pattern_day_trading():
        return

    logging.info("Executing trades")

    try:
        account = api.get_account()
        balance = float(account.cash)
        investment_per_stock = balance * 0.3
    except Exception as e:
        logging.error(f"Error fetching account balance: {e}")
        return

    for ticker in tickers:
        ticker_data = data[data['Ticker'] == ticker]
        if ticker_data.empty:
            logging.warning(f"No data for ticker {ticker}. Skipping.")
            continue

        for index, row in ticker_data.iterrows():
            position_qty = 0
            try:
                position = api.get_position(ticker)
                position_qty = int(position.qty)
            except Exception:
                pass  # No current position

            if row['Signal'] == 1:  # Buy Signal
                qty_to_buy = int(investment_per_stock / row['Close'])
                if qty_to_buy > 0:
                    try:
                        api.submit_order(
                            symbol=ticker,
                            qty=qty_to_buy,
                            side='buy',
                            type='market',
                            time_in_force='gtc'
                        )
                        logging.info(f"Bought {qty_to_buy} shares of {ticker} at {row['Close']}")
                    except Exception as e:
                        logging.error(f"Error executing buy order for {ticker}: {e}")

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

# Send Daily Report
def send_sms_report(report):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=report,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        logging.info(f"Daily report SMS sent successfully. SID: {message.sid}")
    except Exception as e:
        logging.error(f"Error sending SMS report: {e}")

def send_email_report(subject, body, to_email):
    # Email configuration
    from_email =  FROM_EMAIL  # Your email
    from_password = FROM_PASSWORD  # Your email password (or app password for Gmail)
    
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Create a server instance
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        
        # Log in to your Gmail account
        server.login(from_email, from_password)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        
        # Close the server connection
        server.quit()
        
        logging.info(f"Daily report email sent successfully to {to_email}")
    
    except Exception as e:
        logging.error(f"Error sending email report: {e}")
        
# Generate Daily Report
def generate_daily_report(data):
    if data.empty:
        logging.error("Data is empty. Cannot generate report.")
        return "No data available to generate report."

    # Ensure we get scalar values by accessing the first and last entry in the 'Close' column
    first_close = data['Close'].iloc[0] if not data['Close'].iloc[0] is np.nan else None
    last_close = data['Close'].iloc[-1] if not data['Close'].iloc[-1] is np.nan else None

    # Check for NaN values and handle them
    if first_close is None or last_close is None:
        logging.warning("Missing data in 'Close' prices. Cannot calculate profit/loss.")
        return "Profit/Loss calculation failed due to missing data."

    # Calculate profit/loss as a scalar
    profit_loss = last_close - first_close

    # Ensure 'tickers' is a string, not a pandas Series
    tickers = ', '.join(data['Ticker'].unique().astype(str))  # Make sure tickers are joined as a string

    pfloss = pd.Series(profit_loss)
    formatted_pfloss = pfloss.apply(lambda x: '{:.2f}'.format(x))

    # Create the report, ensure profit_loss is formatted as a scalar
    report = f"Daily Trading Report:\nTickers: {tickers}\nProfit/Loss: {formatted_pfloss}\n"
    return report

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
    #send_sms_report_v2(report)

if __name__ == "__main__":
    main()
