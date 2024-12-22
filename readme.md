# AI Stock Agent

This project is an AI-based stock trading agent that fetches stock data, performs feature engineering, generates trade signals, executes trades, and sends daily reports via SMS and email.

## Project Structure

ai-stock-agent/ 
├── data_fetcher.py 
├── feature_engineering.py 
├── trade_executor.py 
├── report_generator.py 
├── notifier.py 
├── app.py 
├── .env 
├── requirements.txt 
└── README.md

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/chand-uma/ai-stock-agent.git
    cd ai-stock-agent
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a [.env](http://_vscodecontentref_/4) file in the root directory and add your environment variables:
    ```plaintext
    ALPACA_API_KEY=your_alpaca_api_key
    ALPACA_SECRET_KEY=your_alpaca_secret_key
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_phone_number
    RECIPIENT_PHONE_NUMBER=recipient_phone_number
    EMAIL_ADDRESS=your_email_address
    EMAIL_PASSWORD=your_email_password
    SMTP_SERVER=smtp.your_email_provider.com
    SMTP_PORT=587
    ```

4. Run the application:
    ```bash
    python app.py
    ```

## Usage

- The application fetches stock data for the specified tickers, performs feature engineering, generates trade signals, executes trades, and sends daily reports via SMS and email.
- Modify the tickers in [app.py](http://_vscodecontentref_/5) to fetch data for different stocks.
- Uncomment the `send_sms_report` and `send_email_report` lines in [app.py](http://_vscodecontentref_/6) to enable SMS and email notifications.

## License

This project is licensed under the MIT License.