import sqlite3
import os
import sys

def get_db_path():
    # Get the absolute path of the project root
    project_root = os.path.abspath(os.path.dirname(__file__))
    # Path to the database file
    db_path = os.path.join(project_root, 'roadmaster.db')
    return db_path

def view_all_bookings():
    try:
        # Connect to the database
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute a query to get all bookings
        cursor.execute("SELECT * FROM bookings")
        
        # Fetch all results
        bookings = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Print header
        print("\n=== ALL BOOKINGS ===")
        print(f"Total bookings: {len(bookings)}")
        print("-" * 80)
        
        # Format as a table
        format_str = "{:<5} {:<20} {:<15} {:<25} {:<20} {:<20}"
        print(format_str.format(*column_names))
        print("-" * 80)
        
        # Print each booking
        for booking in bookings:
            print(format_str.format(*[str(item) for item in booking]))
        
        # Close connection
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_all_bookings() 