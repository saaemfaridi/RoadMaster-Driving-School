import logging
import os
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

# Get configuration from environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'roadmaster@example.com')

def send_sms(to_number, message):
    """Send SMS notification using Twilio"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        logger.error("Twilio credentials not configured")
        return False
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Send the message
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        
        logger.info(f"SMS sent to {to_number}: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Error sending SMS to {to_number}: {e}")
        return False

def send_email(to_email, subject, message_body, is_html=False):
    """Send email notification"""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.error("SMTP credentials not configured")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach message body
        if is_html:
            msg.attach(MIMEText(message_body, 'html'))
        else:
            msg.attach(MIMEText(message_body, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {e}")
        return False

def send_notification(user, subject, message, notification_type='all'):
    """Send notification to user based on their preferences"""
    success = True
    
    if notification_type in ['all', 'email'] and user.email:
        email_success = send_email(user.email, subject, message)
        if not email_success:
            success = False
    
    if notification_type in ['all', 'sms'] and user.phone_number:
        sms_success = send_sms(user.phone_number, message)
        if not sms_success:
            success = False
    
    return success 