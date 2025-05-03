from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Base
from config import DATABASE_URI

def init_db():
    """Initialize the database with tables defined in models.py"""
    try:
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        print("Database tables created successfully!")
        
        # Create a session for potential initial data seeding
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Seed initial data if needed
        # seed_data(session)
        
        session.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def seed_data(session):
    """Seed the database with initial data"""
    # Example code to add initial data if needed
    # from database.models import User
    # admin = User(username="admin", email="admin@example.com", password_hash="hashed_password")
    # session.add(admin)
    # session.commit()
    pass

if __name__ == "__main__":
    init_db() 