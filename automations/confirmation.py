import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Twilio credentials from environment variables or use placeholder values
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')  # Twilio sandbox number

def format_booking_details(booking):
    """Format booking details into a human-readable message"""
    # Format date and time for better readability
    formatted_datetime = booking.slot_datetime.strftime('%A, %B %d, %Y at %I:%M %p')
    
    # Build the message
    message = f"""
*Booking Confirmation - RoadMaster*

Dear {booking.name},

Your driving lesson has been booked successfully!

*Booking Details:*
• *Lesson Type:* {booking.lesson_type}
• *Date & Time:* {formatted_datetime}
• *Booking ID:* {booking.id}

Please arrive 10 minutes before your scheduled time. 
If you need to reschedule, please call us at least 24 hours in advance.

Thank you for choosing RoadMaster!
"""
    return message

def send_confirmation(booking):
    """
    Send a WhatsApp confirmation message for a booking.
    If WhatsApp fails, automatically falls back to SMS.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.warning("Twilio credentials not configured. WhatsApp confirmation not sent.")
        return {"success": False, "message": "Twilio credentials not configured"}
    
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format the message
        message_body = format_booking_details(booking)
        
        # Format the recipient's phone number for WhatsApp
        # Remove any non-digit characters except the leading +
        clean_phone = ''.join(char for char in booking.phone if char.isdigit() or char == '+')
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
        
        recipient = f"whatsapp:{clean_phone}"
        
        # Send the message
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_FROM,
            to=recipient
        )
        
        logger.info(f"WhatsApp confirmation sent to {recipient}. SID: {message.sid}")
        return {
            "success": True, 
            "message": "WhatsApp confirmation sent successfully",
            "sid": message.sid
        }
        
    except TwilioRestException as e:
        logger.warning(f"Twilio API error sending WhatsApp: {str(e)}. Error code: {e.code}. Falling back to SMS.")
        
        # Automatically fall back to SMS
        sms_result = send_confirmation_sms(booking)
        
        if sms_result["success"]:
            return {
                "success": True,
                "message": "WhatsApp failed but SMS sent successfully",
                "fallback": "sms",
                "sid": sms_result.get("sid", ""),
                "original_error": str(e)
            }
        else:
            return {
                "success": False,
                "message": "Both WhatsApp and SMS failed",
                "whatsapp_error": str(e),
                "sms_error": sms_result.get("message", "")
            }
    
    except Exception as e:
        logger.error(f"Error sending WhatsApp confirmation: {str(e)}")
        
        # Try SMS as fallback for any error
        try:
            logger.info("Attempting SMS fallback...")
            sms_result = send_confirmation_sms(booking)
            
            if sms_result["success"]:
                return {
                    "success": True,
                    "message": "WhatsApp failed but SMS sent successfully",
                    "fallback": "sms",
                    "sid": sms_result.get("sid", ""),
                    "original_error": str(e)
                }
            else:
                return {
                    "success": False,
                    "message": "Both WhatsApp and SMS failed",
                    "whatsapp_error": str(e),
                    "sms_error": sms_result.get("message", "")
                }
        except Exception as sms_error:
            logger.error(f"SMS fallback also failed: {str(sms_error)}")
            return {
                "success": False,
                "message": "Both WhatsApp and SMS failed",
                "whatsapp_error": str(e),
                "sms_error": str(sms_error)
            }

def send_confirmation_sms(booking):
    """Send a regular SMS confirmation message (fallback method)"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.warning("Twilio credentials not configured. SMS confirmation not sent.")
        return {"success": False, "message": "Twilio credentials not configured"}
    
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format the message for SMS (simpler version)
        formatted_datetime = booking.slot_datetime.strftime('%m/%d/%Y at %I:%M %p')
        message_body = f"RoadMaster Confirmation: Your {booking.lesson_type} is scheduled for {formatted_datetime}. Booking ID: {booking.id}. Thank you!"
        
        # Format the recipient's phone number
        clean_phone = ''.join(char for char in booking.phone if char.isdigit() or char == '+')
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
        
        # Get the Twilio phone number from environment or use placeholder
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER', '')
        
        if not twilio_phone:
            logger.warning("Twilio phone number not configured. SMS confirmation not sent.")
            return {"success": False, "message": "Twilio phone number not configured"}
        
        # Send the message
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone,
            to=clean_phone
        )
        
        logger.info(f"SMS confirmation sent to {clean_phone}. SID: {message.sid}")
        return {
            "success": True, 
            "message": "SMS confirmation sent successfully",
            "sid": message.sid
        }
        
    except Exception as e:
        logger.error(f"Error sending SMS confirmation: {str(e)}")
        return {"success": False, "message": str(e)} 