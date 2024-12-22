import logging
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_sms_report(report):
    """
    Send the daily report via SMS using Twilio.
    """
    try:
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        message = client.messages.create(
            body=report,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=os.getenv('RECIPIENT_PHONE_NUMBER')
        )
        logging.info(f"Daily report SMS sent successfully. SID: {message.sid}")
    except Exception as e:
        logging.error(f"Error sending SMS report: {e}")

def send_email_report(subject, body, to_email):
    """
    Send the daily report via email.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL_ADDRESS')
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
        server.starttls()
        server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
        text = msg.as_string()
        server.sendmail(os.getenv('EMAIL_ADDRESS'), to_email, text)
        server.quit()
        logging.info("Daily report email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email report: {e}")