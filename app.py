from flask import Flask, render_template, request, jsonify, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import os
from datetime import datetime
import re

# Initialize Flask app
app = Flask(__name__, 
            static_folder='frontend/static',
            template_folder='frontend/templates')

# Load configuration
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key'),
    DATABASE_URI=os.environ.get('DATABASE_URI', 'sqlite:///database/roadmaster.db'),
    OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY', ''),
    TWILIO_ACCOUNT_SID=os.environ.get('TWILIO_ACCOUNT_SID', ''),
    TWILIO_AUTH_TOKEN=os.environ.get('TWILIO_AUTH_TOKEN', '')
)

# Initialize SQLAlchemy database
from backend.models import db, init_db, Booking
init_db(app)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Import routes after app initialization to avoid circular imports
from backend.routes import main_routes, api_routes

# Import WhatsApp confirmation module
from automations.confirmation import send_confirmation, send_confirmation_sms

# Register blueprints
app.register_blueprint(main_routes)
app.register_blueprint(api_routes, url_prefix='/api')

# Booking form route
@app.route('/book', methods=['GET', 'POST'])
def book_lesson():
    # For GET requests, pass today's date for client-side validation
    if request.method == 'GET':
        today_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('book.html', today_date=today_date)
    
    # For POST requests, process form data
    if request.method == 'POST':
        # Determine if the request wants JSON response
        wants_json = request.headers.get('Accept') == 'application/json' or request.is_json
        
        # Get form or JSON data
        if request.is_json:
            data = request.json
            name = data.get('name')
            phone = data.get('phone')
            lesson_type = data.get('lesson_type')
            
            # For API requests that directly provide slot_datetime
            slot_datetime_str = data.get('slot_datetime')
            if slot_datetime_str:
                slot_date = None
                slot_time = None
            else:
                slot_date = data.get('slot_date')
                slot_time = data.get('slot_time')
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            lesson_type = request.form.get('lesson_type')
            slot_date = request.form.get('slot_date')
            slot_time = request.form.get('slot_time')
            slot_datetime_str = None
        
        # Initialize structured validation result
        validation = {
            "valid": True,
            "errors": {
                "name": None,
                "phone": None,
                "lesson_type": None,
                "date_time": None
            },
            "error_messages": []
        }
        
        # Validate name (at least 3 characters)
        if not name or len(name) < 3:
            validation["valid"] = False
            validation["errors"]["name"] = "Name must be at least 3 characters long"
            validation["error_messages"].append("Name must be at least 3 characters long")
        
        # Validate phone number (10-15 digits, can start with +)
        phone_pattern = re.compile(r'^\+?[0-9]{10,15}$')
        if not phone or not phone_pattern.match(phone):
            validation["valid"] = False
            validation["errors"]["phone"] = "Please enter a valid phone number (10-15 digits, can start with +)"
            validation["error_messages"].append("Please enter a valid phone number")
        
        # Validate lesson type
        if not lesson_type:
            validation["valid"] = False
            validation["errors"]["lesson_type"] = "Please select a lesson type"
            validation["error_messages"].append("Please select a lesson type")
        
        # Validate date and time
        slot_datetime = None
        
        # If slot_datetime_str is provided directly (from API)
        if slot_datetime_str:
            try:
                slot_datetime = datetime.strptime(slot_datetime_str, '%Y-%m-%d %H:%M:%S')
                
                # Check if date is in the future
                if slot_datetime < datetime.now():
                    validation["valid"] = False
                    validation["errors"]["date_time"] = "Please select a future date and time"
                    validation["error_messages"].append("Please select a future date and time")
            except ValueError:
                validation["valid"] = False
                validation["errors"]["date_time"] = "Invalid date time format. Use YYYY-MM-DD HH:MM:SS"
                validation["error_messages"].append("Invalid date time format")
        
        # If slot_date and slot_time are provided (from form)
        elif slot_date and slot_time:
            try:
                slot_datetime_str = f"{slot_date} {slot_time}:00"
                slot_datetime = datetime.strptime(slot_datetime_str, '%Y-%m-%d %H:%M:%S')
                
                # Check if date is in the future
                if slot_datetime < datetime.now():
                    validation["valid"] = False
                    validation["errors"]["date_time"] = "Please select a future date and time"
                    validation["error_messages"].append("Please select a future date and time")
            except ValueError:
                validation["valid"] = False
                validation["errors"]["date_time"] = "Invalid date or time format"
                validation["error_messages"].append("Invalid date or time format")
        else:
            validation["valid"] = False
            validation["errors"]["date_time"] = "Please select a valid date and time"
            validation["error_messages"].append("Please select a valid date and time")
        
        # If there are validation errors
        if not validation["valid"]:
            if wants_json:
                return jsonify({
                    "status": "error",
                    "message": "Validation failed",
                    "validation": validation
                }), 400
            else:
                # For web form, pass today's date for client-side validation
                today_date = datetime.now().strftime('%Y-%m-%d')
                return render_template('book.html', 
                                      message=', '.join(validation["error_messages"]), 
                                      message_type='danger',
                                      today_date=today_date)
        
        # If validation passes, create a new booking
        try:
            new_booking = Booking(
                name=name,
                phone=phone,
                lesson_type=lesson_type,
                slot_datetime=slot_datetime
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            # Send WhatsApp confirmation
            confirmation_result = send_confirmation(new_booking)
            
            # If WhatsApp fails, try SMS as fallback
            if not confirmation_result["success"]:
                sms_result = send_confirmation_sms(new_booking)
                if sms_result["success"]:
                    confirmation_message = "Booking confirmed. A confirmation SMS has been sent to your phone."
                    confirmation_status = "sms_sent"
                else:
                    confirmation_message = "Booking confirmed. However, we couldn't send a confirmation message to your phone."
                    confirmation_status = "failed"
            else:
                confirmation_message = "Booking confirmed. A WhatsApp confirmation has been sent to your phone."
                confirmation_status = "whatsapp_sent"
            
            # Prepare the booking data for the response
            booking_data = {
                "id": new_booking.id,
                "name": new_booking.name,
                "phone": new_booking.phone,
                "lesson_type": new_booking.lesson_type,
                "slot_datetime": new_booking.slot_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                "created_at": new_booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Return JSON response if requested
            if wants_json:
                return jsonify({
                    "status": "success",
                    "message": "Booking created successfully",
                    "booking_id": new_booking.id,
                    "confirmation_status": confirmation_status,
                    "booking": booking_data
                }), 201
            
            # For regular form submissions
            return render_template('book.html', 
                                  message=confirmation_message, 
                                  message_type='success',
                                  today_date=datetime.now().strftime('%Y-%m-%d'))
            
        except Exception as e:
            db.session.rollback()
            
            if wants_json:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 500
            
            return render_template('book.html', 
                                  message=f'An error occurred: {str(e)}', 
                                  message_type='danger',
                                  today_date=datetime.now().strftime('%Y-%m-%d'))

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if scheduler.running:
        scheduler.shutdown()

if __name__ == '__main__':
    app.run(debug=True) 