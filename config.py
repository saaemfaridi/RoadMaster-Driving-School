import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
PORT = int(os.environ.get('FLASK_PORT', 5000))

# Database configuration
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///database/roadmaster.db')

# External API keys
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')

# Scheduler configuration
SCHEDULER_API_ENABLED = True

# Application paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, 'templates')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static') 