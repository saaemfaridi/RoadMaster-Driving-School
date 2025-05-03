# RoadMaster - Driving School Management System

RoadMaster is a Flask-based web application for managing a driving school's bookings and operations.

## Features

- Book driving lessons through a web interface
- Manage bookings through a dashboard
- Automated WhatsApp/SMS notifications for booking confirmations
- RESTful API for integration with other systems
- Streamlit interface for easy booking management

## Project Structure

```
RoadMaster/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── roadmaster.db           # SQLite database
├── streamlit_booking.py    # Streamlit booking interface
├── view_bookings.py        # Viewing bookings interface
├── run_tests.py            # Test runner script
├── test_app.py             # Unit tests for Flask app
├── test_streamlit_app.py   # Tests for Streamlit integration
├── automations/            # Automation scripts
│   └── confirmation.py     # WhatsApp/SMS notifications
├── backend/                # Backend code
│   ├── models.py           # Database models
│   └── routes.py           # API routes and endpoints
├── database/               # Database files
├── docs/                   # Documentation
│   ├── api.md              # API documentation
│   ├── system_design.md    # System design documentation
│   └── setup.md            # Setup instructions
└── frontend/               # Frontend code
    ├── static/             # Static assets (CSS, JS)
    └── templates/          # HTML templates
        ├── home.html       # Homepage
        ├── book.html       # Booking form
        └── dashboard.html  # Admin dashboard
```

## Prerequisites

- Python 3.8+
- Flask
- SQLAlchemy
- Twilio account (for WhatsApp/SMS)
- Streamlit (for admin interface)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/roadmaster.git
   cd roadmaster
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file with your configuration:
   ```
   SECRET_KEY=your_secret_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

## Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```

2. Access the web interface at: http://127.0.0.1:5000

3. Run the Streamlit interface (in a separate terminal):
   ```
   streamlit run streamlit_booking.py
   ```

## Testing the Application

The project includes several test scripts to help you test different aspects of the application.

### Test Runner

For convenience, a test runner script is provided that can run various tests:

```
python run_tests.py
```

This script provides the following options:

1. **Unit tests only** - Tests the Flask application functionality
2. **Integration tests only** - Tests the Streamlit integration (requires manual setup)
3. **Full test suite** - Runs all tests and starts required servers automatically
4. **Manual testing** - Starts both Flask and Streamlit servers for manual testing

### Running Tests Individually

To run specific tests:

1. **Flask application tests**:
   ```
   python test_app.py
   ```

2. **Streamlit integration tests** (Flask app must be running):
   ```
   python test_streamlit_app.py
   ```

### What to Test

When testing the application, you should verify:

1. **Booking Creation**:
   - Can you create bookings through the web form?
   - Are validation rules working properly?
   - Is data saved correctly in the database?

2. **API Functionality**:
   - Do the API endpoints return correct responses?
   - Can you create, read, update, and delete bookings via API?

3. **WhatsApp/SMS Notifications**:
   - Are confirmation messages sent when bookings are created?
   - Do the fallback mechanisms work if primary method fails?

4. **Streamlit Interface**:
   - Can you create bookings through the Streamlit interface?
   - Does it properly communicate with the Flask backend?

## API Documentation

The RoadMaster API provides the following endpoints:

### Status Endpoint

#### Check API Status
```
GET /api/status
```

Response:
```json
{
  "status": "ok"
}
```

Example usage with curl:
```bash
curl http://localhost:5000/api/status
```

### Booking Endpoints

#### Get All Bookings
```
GET /api/bookings
```

Response:
```json
{
  "bookings": [
    {
      "id": 1,
      "name": "John Doe",
      "phone": "+1234567890",
      "lesson_type": "Standard",
      "slot_datetime": "2023-12-01 10:00:00",
      "created_at": "2023-11-15 10:30:00"
    }
  ]
}
```

Example usage with curl:
```bash
curl http://localhost:5000/api/bookings
```

Example usage in Python:
```python
import requests
response = requests.get('http://localhost:5000/api/bookings')
bookings = response.json()['bookings']
```

#### Get a Specific Booking
```
GET /api/bookings/<id>
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "lesson_type": "Standard",
  "slot_datetime": "2023-12-01 10:00:00",
  "created_at": "2023-11-15 10:30:00"
}
```

Example usage with curl:
```bash
curl http://localhost:5000/api/bookings/1
```

#### Create a New Booking
```
POST /api/bookings
Content-Type: application/json

{
  "name": "Jane Smith",
  "phone": "+1987654321",
  "lesson_type": "Advanced",
  "slot_datetime": "2023-12-05 14:00:00"
}
```

Response:
```json
{
  "id": 2,
  "name": "Jane Smith",
  "phone": "+1987654321",
  "lesson_type": "Advanced",
  "slot_datetime": "2023-12-05 14:00:00",
  "created_at": "2023-11-16 09:45:00"
}
```

Example usage with curl:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Jane Smith", "phone": "+1987654321", "lesson_type": "Advanced", "slot_datetime": "2023-12-05 14:00:00"}' http://localhost:5000/api/bookings
```

Example usage in Python:
```python
import requests
data = {
    "name": "Jane Smith",
    "phone": "+1987654321",
    "lesson_type": "Advanced",
    "slot_datetime": "2023-12-05 14:00:00"
}
response = requests.post('http://localhost:5000/api/bookings', json=data)
booking = response.json()
```

#### Update a Booking
```
PUT /api/bookings/<id>
Content-Type: application/json

{
  "lesson_type": "Premium",
  "slot_datetime": "2023-12-05 16:00:00"
}
```

Response:
```json
{
  "id": 2,
  "name": "Jane Smith",
  "phone": "+1987654321",
  "lesson_type": "Premium",
  "slot_datetime": "2023-12-05 16:00:00",
  "created_at": "2023-11-16 09:45:00"
}
```

Example usage with curl:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"lesson_type": "Premium", "slot_datetime": "2023-12-05 16:00:00"}' http://localhost:5000/api/bookings/2
```

#### Delete a Booking
```
DELETE /api/bookings/<id>
```

Response:
```json
{
  "message": "Booking deleted successfully"
}
```

Example usage with curl:
```bash
curl -X DELETE http://localhost:5000/api/bookings/2
```

### Streamlit Integration Endpoint

#### Create a Booking with Notification
```
POST /api/booking
Content-Type: application/json

{
  "name": "Alex Johnson",
  "phone": "+1567890123",
  "lesson_type": "Standard",
  "slot_datetime": "2023-12-10 11:00:00"
}
```

Response:
```json
{
  "status": "success",
  "message": "Booking created successfully",
  "booking_id": 3,
  "confirmation_status": "whatsapp_sent",
  "confirmation_details": {
    "success": true,
    "message": "WhatsApp confirmation sent successfully",
    "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "booking": {
    "id": 3,
    "name": "Alex Johnson",
    "phone": "+1567890123",
    "lesson_type": "Standard",
    "slot_datetime": "2023-12-10 11:00:00",
    "created_at": "2023-11-20 14:20:00"
  }
}
```

This endpoint is specifically designed for the Streamlit integration and includes the following features:
- Automatic WhatsApp notification
- SMS fallback if WhatsApp fails
- Detailed confirmation status information
- Complete booking information in the response

Example usage in Python (Streamlit):
```python
import requests
import datetime

def create_booking(name, phone, lesson_type, slot_datetime):
    data = {
        "name": name,
        "phone": phone,
        "lesson_type": lesson_type,
        "slot_datetime": slot_datetime.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        response = requests.post('http://localhost:5000/api/booking', json=data)
        return response.json(), response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, 500
```

## Templates

The web interface is built using three main HTML templates:

### home.html - Landing Page

The home page provides information about the driving school services and links to the booking form.

Features:
- Hero section with call-to-action button
- Service cards for different lesson types
- "Why choose us" section
- Mobile-responsive design

Example usage:
```python
@main_routes.route('/')
def index():
    return render_template('home.html')
```

### book.html - Booking Form

The booking form allows users to schedule driving lessons with validation.

Features:
- Form with personal information fields
- Lesson type selection
- Date and time picker
- Client-side JavaScript validation
- Server-side validation
- Success/error message display
- Terms and conditions modal

Example usage:
```python
@main_routes.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        today_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('book.html', today_date=today_date)
    
    # POST request handling for form submission
    # ...
```

Form submission example:
```html
<form id="bookingForm" action="/book" method="POST" class="needs-validation" novalidate>
    <input type="text" name="name" required minlength="3">
    <input type="tel" name="phone" required pattern="^\+?[0-9]{10,15}$">
    <select name="lesson_type" required>
        <option value="Standard">Standard Lesson</option>
        <option value="Advanced">Advanced Lesson</option>
        <option value="Premium">Premium Package</option>
    </select>
    <input type="date" name="slot_date" required>
    <select name="slot_time" required>
        <option value="09:00">9:00 AM</option>
        <!-- other time options -->
    </select>
    <button type="submit">Book Now</button>
</form>
```

### dashboard.html - Booking Management

The dashboard displays all bookings with filtering and management options.

Features:
- Statistics cards (total bookings, today's lessons, etc.)
- Filterable and searchable table of bookings
- Booking details modal
- Delete booking functionality
- CSV export option
- AJAX data refresh

Example usage:
```python
@main_routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
```

JavaScript interaction with API:
```javascript
// Example of fetching bookings from the API
function fetchBookings() {
    fetch('/api/bookings')
        .then(response => response.json())
        .then(data => {
            updateBookingsTable(data.bookings);
            updateStats(data.bookings);
        })
        .catch(error => {
            console.error('Error fetching bookings:', error);
        });
}
```

## License

[MIT License](LICENSE)