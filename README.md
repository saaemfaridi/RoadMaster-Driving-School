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
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── roadmaster.db         # SQLite database
├── streamlit_booking.py  # Streamlit booking interface
├── view_bookings.py      # Viewing bookings interface
├── automations/         # Automation scripts
│   └── confirmation.py  # WhatsApp/SMS notifications
├── backend/            # Backend code
│   ├── models.py      # Database models
│   └── routes.py      # API routes and endpoints
├── database/          # Database files
└── frontend/          # Frontend code
    ├── static/        # Static assets (CSS, JS)
    └── templates/     # HTML templates
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

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
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

## API Documentation

The RoadMaster API provides endpoints for managing bookings. For detailed API documentation, please refer to the API documentation in the `/docs` directory.

## License

[MIT License](LICENSE)