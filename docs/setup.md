# RoadMaster Setup Guide

## Project Overview

RoadMaster is a Flask-based web application for managing roadside assistance operations. The application includes features for task management, automated notifications, and reporting.

## Prerequisites

- Python 3.8+ installed
- pip (Python package manager)
- Virtual environment tool (venv or similar)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd roadmaster
```

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```
# Flask configuration
SECRET_KEY=your_secret_key
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database configuration
DATABASE_URI=sqlite:///database/roadmaster.db

# External API keys
OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone

# SMTP configuration (for email notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_email_password
EMAIL_FROM=noreply@roadmaster.com
```

### 5. Initialize the Database

```bash
python -m database.init_db
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Project Structure

- `app.py` - Main application entry point
- `config.py` - Configuration settings
- `/backend` - Flask backend code
- `/frontend` - Templates and static files
- `/database` - Database models and initialization scripts
- `/automations` - Scheduled tasks and automation scripts
- `/docs` - Documentation files

## Development Workflow

1. Activate the virtual environment
2. Make your code changes
3. Run the application for testing
4. Create tests as appropriate

## Deployment

For production deployment, consider:

1. Using Gunicorn as a WSGI server
2. Setting up a reverse proxy with Nginx
3. Using a production-grade database (PostgreSQL, MySQL)
4. Setting up proper logging
5. Using environment variables for configuration

## Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- APScheduler Documentation: https://apscheduler.readthedocs.io/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Twilio Documentation: https://www.twilio.com/docs
- OpenAI Documentation: https://platform.openai.com/docs 