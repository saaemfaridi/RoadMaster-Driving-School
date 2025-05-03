# RoadMaster System Design

## Architecture Overview

RoadMaster is a driving school management system implemented using a multi-tier architecture:

1. **Frontend Tier**
   - Web-based UI built with HTML, CSS, and JavaScript
   - Bootstrap for responsive design
   - Jinja2 templates for server-side rendering

2. **Backend Tier**
   - Flask web framework
   - RESTful API endpoints
   - SQLAlchemy ORM for database operations
   - Blueprint-based route organization

3. **Persistence Tier**
   - SQLite database (for development)
   - Data models for bookings and other entities

4. **Integration Tier**
   - Twilio API for WhatsApp/SMS notifications
   - Streamlit for alternative admin interface

## Database Schema

### Bookings Table
- `id` (Integer, PK): Unique identifier for the booking
- `name` (String): Customer's full name
- `phone` (String): Customer's phone number
- `lesson_type` (String): Type of driving lesson
- `slot_datetime` (DateTime): Date and time of the booking
- `created_at` (DateTime): When the booking record was created

## API Endpoints

### Status Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Check if the API is online |

### Booking Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings` | Get all bookings |
| GET | `/api/bookings/<id>` | Get a specific booking by ID |
| POST | `/api/bookings` | Create a new booking |
| PUT | `/api/bookings/<id>` | Update an existing booking |
| DELETE | `/api/bookings/<id>` | Delete a booking |
| POST | `/api/booking` | Streamlit integration endpoint for creating bookings with notification handling |

### Sample Requests and Responses

#### Create a Booking (POST /api/bookings)

Request:
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "lesson_type": "Standard",
  "slot_datetime": "2023-12-01 10:00:00"
}
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

#### Create a Booking with Notification (POST /api/booking)

Request:
```json
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
  "status": "success",
  "message": "Booking created successfully",
  "booking_id": 2,
  "confirmation_status": "whatsapp_sent",
  "confirmation_details": {
    "success": true,
    "message": "WhatsApp confirmation sent successfully",
    "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "booking": {
    "id": 2,
    "name": "Jane Smith",
    "phone": "+1987654321",
    "lesson_type": "Advanced",
    "slot_datetime": "2023-12-05 14:00:00",
    "created_at": "2023-11-16 09:45:00"
  }
}
```

## Templates

The web interface is built using the following HTML templates:

### home.html
Landing page with service information and links to booking

- Features information about the driving school services
- Cards for Standard, Advanced, and Premium lessons
- Call-to-action buttons linking to the booking form
- Responsive design using Bootstrap

### book.html
Booking form with client-side validation

- Form for collecting customer information
- Validation for name, phone, lesson type, date and time
- Success/error message handling
- Terms and conditions modal
- Client-side validation using JavaScript
- Server-side validation when submitting

### dashboard.html
Table displaying bookings fetched from the API

- Dynamic table of all bookings
- Filtering and searching capabilities
- Booking details view
- Delete confirmation modal
- Statistics cards (total bookings, today's lessons, etc.)
- DataTables integration for advanced table features

## Authentication

Currently, the application does not implement authentication. This is a planned feature for future versions.

## Form Validation

Both client-side and server-side validation are implemented:

### Client-Side Validation
- Name must be at least 3 characters
- Phone must match the pattern `^\+?[0-9]{10,15}$`
- Date must be a future date
- Time must be selected from available slots

### Server-Side Validation
- Same validation rules as client-side
- Structured validation response format
- JSON response for API requests

## Notification System

The application uses Twilio to send booking confirmations:

1. Attempts to send WhatsApp message first
2. If WhatsApp fails, falls back to SMS
3. Proper error handling for all scenarios
4. Logs all notification attempts and results

## Future Enhancements

1. User authentication system
2. Admin/user role separation
3. More sophisticated booking management
4. Calendar view for bookings
5. Email notifications
6. Payment processing integration 