from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from backend.models import db, Booking
from automations.confirmation import send_confirmation, send_confirmation_sms

# Main routes blueprint for web pages
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('home.html')

@main_routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_routes.route('/book')
def book():
    # Pass today's date for the form's date input min attribute
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('book.html', today_date=today_date)

# API routes blueprint for REST endpoints
api_routes = Blueprint('api', __name__)

@api_routes.route('/status')
def status():
    return jsonify({"status": "ok"})

@api_routes.route('/data', methods=['GET'])
def get_data():
    # Example endpoint to get data
    return jsonify({"data": "sample data", "status": "success"})

@api_routes.route('/data', methods=['POST'])
def post_data():
    # Example endpoint to post data
    data = request.json
    # Process data here
    return jsonify({"status": "received", "data": data})

# Booking routes
@api_routes.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    result = []
    for booking in bookings:
        result.append({
            'id': booking.id,
            'name': booking.name,
            'phone': booking.phone,
            'lesson_type': booking.lesson_type,
            'slot_datetime': booking.slot_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({"bookings": result})

@api_routes.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify({
        'id': booking.id,
        'name': booking.name,
        'phone': booking.phone,
        'lesson_type': booking.lesson_type,
        'slot_datetime': booking.slot_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@api_routes.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    
    try:
        slot_datetime = datetime.strptime(data['slot_datetime'], '%Y-%m-%d %H:%M:%S')
        
        new_booking = Booking(
            name=data['name'],
            phone=data['phone'],
            lesson_type=data['lesson_type'],
            slot_datetime=slot_datetime
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({
            'id': new_booking.id,
            'name': new_booking.name,
            'phone': new_booking.phone,
            'lesson_type': new_booking.lesson_type,
            'slot_datetime': new_booking.slot_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': new_booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api_routes.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    data = request.json
    
    try:
        if 'name' in data:
            booking.name = data['name']
        if 'phone' in data:
            booking.phone = data['phone']
        if 'lesson_type' in data:
            booking.lesson_type = data['lesson_type']
        if 'slot_datetime' in data:
            booking.slot_datetime = datetime.strptime(data['slot_datetime'], '%Y-%m-%d %H:%M:%S')
        
        db.session.commit()
        
        return jsonify({
            'id': booking.id,
            'name': booking.name,
            'phone': booking.phone,
            'lesson_type': booking.lesson_type,
            'slot_datetime': booking.slot_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api_routes.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    try:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Booking deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api_routes.route('/booking', methods=['POST'])
def api_booking():
    """API endpoint for creating a booking (for Streamlit integration)"""
    data = request.json
    
    # Basic validation
    required_fields = ['name', 'phone', 'lesson_type', 'slot_datetime']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        # Parse the datetime string
        slot_datetime = datetime.strptime(data['slot_datetime'], '%Y-%m-%d %H:%M:%S')
        
        # Create a new booking
        new_booking = Booking(
            name=data['name'],
            phone=data['phone'],
            lesson_type=data['lesson_type'],
            slot_datetime=slot_datetime
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        # Send confirmation with automatic SMS fallback
        confirmation_result = send_confirmation(new_booking)
        
        # Set confirmation status based on result
        if not confirmation_result["success"]:
            confirmation_status = "failed"
        elif "fallback" in confirmation_result and confirmation_result["fallback"] == "sms":
            confirmation_status = "sms_sent"
        else:
            confirmation_status = "whatsapp_sent"
        
        return jsonify({
            "status": "success",
            "message": "Booking created successfully",
            "booking_id": new_booking.id,
            "confirmation_status": confirmation_status,
            "confirmation_details": confirmation_result,
            "booking": {
                "id": new_booking.id,
                "name": new_booking.name,
                "phone": new_booking.phone,
                "lesson_type": new_booking.lesson_type,
                "slot_datetime": new_booking.slot_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                "created_at": new_booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500 