import streamlit as st
import requests
import datetime
import pandas as pd
from dateutil import parser
import json
import time
import re

# API Base URL
BASE_URL = "http://localhost:5000/api"
BOOKINGS_URL = f"{BASE_URL}/bookings"
BOOKING_URL = f"{BASE_URL}/booking"  # For streamlit integration endpoint

# Page Configuration
st.set_page_config(
    page_title="RoadMaster - Driving School",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to fetch all bookings
def fetch_bookings():
    """Fetch all bookings from the API"""
    try:
        response = requests.get(BOOKINGS_URL)
        if response.status_code == 200:
            return response.json()["bookings"], None
        else:
            return None, f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return None, f"Connection error: {str(e)}"

# Function to create a new booking
def create_booking(name, phone, lesson_type, slot_datetime):
    """Create a booking through the API"""
    data = {
        "name": name,
        "phone": phone,
        "lesson_type": lesson_type,
        "slot_datetime": slot_datetime.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        response = requests.post(BOOKINGS_URL, json=data, headers={"Accept": "application/json"})
        return response.json(), response.status_code
    except requests.RequestException as e:
        return {"error": str(e)}, 500

# Function to delete a booking
def delete_booking(booking_id):
    """Delete a booking through the API"""
    try:
        response = requests.delete(f"{BOOKINGS_URL}/{booking_id}")
        if response.status_code == 200:
            return True, "Booking deleted successfully"
        else:
            return False, f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return False, f"Connection error: {str(e)}"

# Function to format datetime for display
def format_datetime(datetime_str):
    """Format datetime string for display"""
    try:
        dt = parser.parse(datetime_str)
        return dt.strftime("%b %d, %Y %I:%M %p")
    except:
        return datetime_str

# Sidebar
st.sidebar.image("https://www.svgrepo.com/show/530453/road-map.svg", width=100)
st.sidebar.title("RoadMaster")
st.sidebar.subheader("Driving School Management")

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Book a Lesson"])

# Server status
server_status = "Online" if requests.get(f"{BASE_URL}/status").status_code == 200 else "Offline"
st.sidebar.metric("Server Status", server_status, delta="Connected" if server_status == "Online" else "Disconnected")

# Current time
st.sidebar.write(f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Instructions
with st.sidebar.expander("Instructions"):
    st.write("""
    To use this application:
    1. Make sure the Flask server is running:
       ```
       python app.py
       ```
    2. The server should be accessible at http://localhost:5000
    """)

# Main content
if page == "Dashboard":
    st.title("🚗 RoadMaster Dashboard")
    
    # Fetch bookings
    with st.spinner("Loading bookings..."):
        bookings, error = fetch_bookings()
    
    if error:
        st.error(error)
    else:
        if not bookings:
            st.info("No bookings found. Create your first booking using the 'Book a Lesson' page.")
        else:
            # Convert to DataFrame for easier filtering and display
            df = pd.DataFrame(bookings)
            
            # Convert datetime columns
            for col in ['slot_datetime', 'created_at']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])
            
            # Extract date and time components for filtering
            if 'slot_datetime' in df.columns:
                df['date'] = df['slot_datetime'].dt.date
                df['time'] = df['slot_datetime'].dt.time
            
            # Create metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Bookings", len(df))
            with col2:
                today_count = len(df[df['date'] == datetime.date.today()]) if 'date' in df.columns else 0
                st.metric("Today's Lessons", today_count)
            with col3:
                # Calculate one week from now
                one_week = datetime.date.today() + datetime.timedelta(days=7)
                this_week = len(df[(df['date'] >= datetime.date.today()) & 
                                  (df['date'] <= one_week)]) if 'date' in df.columns else 0
                st.metric("This Week", this_week)
            with col4:
                lesson_counts = df['lesson_type'].value_counts() if 'lesson_type' in df.columns else {}
                most_popular = lesson_counts.idxmax() if not lesson_counts.empty else "N/A"
                st.metric("Most Popular", most_popular)
            
            # Filters
            st.subheader("Filters")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                date_options = [datetime.date.today()]
                if 'date' in df.columns:
                    date_options = sorted(df['date'].unique())
                selected_date = st.selectbox("Filter by Date", ["All Dates"] + list(date_options))
            
            with col2:
                lesson_options = []
                if 'lesson_type' in df.columns:
                    lesson_options = sorted(df['lesson_type'].unique())
                selected_lesson = st.selectbox("Filter by Lesson Type", ["All Types"] + list(lesson_options))
                
            with col3:
                name_search = st.text_input("Search by Name")
            
            # Apply filters
            filtered_df = df.copy()
            
            if selected_date != "All Dates" and 'date' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['date'] == selected_date]
                
            if selected_lesson != "All Types" and 'lesson_type' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['lesson_type'] == selected_lesson]
                
            if name_search and 'name' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['name'].str.contains(name_search, case=False)]
            
            # Show bookings table
            st.subheader(f"Bookings ({len(filtered_df)})")
            
            if not filtered_df.empty:
                # Format datetime columns for display
                display_df = filtered_df.copy()
                if 'slot_datetime' in display_df.columns:
                    display_df['slot_datetime'] = display_df['slot_datetime'].apply(
                        lambda x: x.strftime("%b %d, %Y %I:%M %p"))
                if 'created_at' in display_df.columns:
                    display_df['created_at'] = display_df['created_at'].apply(
                        lambda x: x.strftime("%b %d, %Y %I:%M %p"))
                
                # Select columns to display
                columns_to_display = ['id', 'name', 'phone', 'lesson_type', 'slot_datetime', 'created_at']
                display_df = display_df[[col for col in columns_to_display if col in display_df.columns]]
                
                # Rename columns for better display
                display_df = display_df.rename(columns={
                    'id': 'ID',
                    'name': 'Name',
                    'phone': 'Phone',
                    'lesson_type': 'Lesson Type',
                    'slot_datetime': 'Date & Time',
                    'created_at': 'Created At'
                })
                
                st.dataframe(display_df, use_container_width=True)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Refresh Data"):
                        st.rerun()
                with col2:
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Export as CSV",
                        csv,
                        "roadmaster_bookings.csv",
                        "text/csv",
                        key='download-csv'
                    )
                
                # Booking details section
                st.subheader("Booking Details")
                selected_id = st.selectbox("Select Booking ID to View Details", 
                                         display_df['ID'].tolist())
                
                if selected_id:
                    # Find the selected booking
                    selected_booking = df[df['id'] == selected_id].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Name:** {selected_booking['name']}")
                        st.markdown(f"**Phone:** {selected_booking['phone']}")
                        st.markdown(f"**Lesson Type:** {selected_booking['lesson_type']}")
                    with col2:
                        st.markdown(f"**Date & Time:** {format_datetime(str(selected_booking['slot_datetime']))}")
                        st.markdown(f"**Created At:** {format_datetime(str(selected_booking['created_at']))}")
                    
                    # Actions
                    if st.button("Delete This Booking"):
                        success, message = delete_booking(selected_id)
                        if success:
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                st.info("No bookings match the current filters.")

elif page == "Book a Lesson":
    st.title("🚗 Book a Driving Lesson")
    st.write("Fill out the form below to book your driving lesson")
    
    # Create booking form
    with st.form("booking_form"):
        # Personal Information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", 
                                help="Enter your full name (minimum 3 characters)")
        with col2:
            phone = st.text_input("Phone Number", 
                                 placeholder="+1234567890",
                                 help="Enter your phone number with country code, e.g., +1234567890")
        
        # Lesson Details
        st.subheader("Lesson Details")
        lesson_types = [
            "Standard",
            "Advanced",
            "Premium"
        ]
        lesson_type = st.selectbox("Lesson Type", lesson_types,
                                  help="Select the type of driving lesson you want to book")
        
        # Date and time selection
        st.subheader("Date and Time")
        col1, col2 = st.columns(2)
        with col1:
            min_date = datetime.date.today()
            date = st.date_input("Date", 
                                min_value=min_date,
                                help="Select the date for your lesson (must be today or later)")
        with col2:
            # Start times between 9 AM and 5 PM
            default_time = datetime.time(9, 0)
            time_options = []
            for hour in range(9, 18):
                time_options.append(datetime.time(hour, 0))
            
            time = st.selectbox("Time", time_options,
                              format_func=lambda x: x.strftime("%I:%M %p"),
                              help="Select the time for your lesson")
        
        # Combine date and time
        slot_datetime = datetime.datetime.combine(date, time)
        
        # Submit button
        submitted = st.form_submit_button("Book Now")
    
    # Form validation and submission
    if submitted:
        errors = []
        
        # Validate name
        if not name or len(name) < 3:
            errors.append("Please enter your full name (minimum 3 characters)")
        
        # Validate phone number (10-15 digits, can start with +)
        phone_pattern = re.compile(r'^\+?[0-9]{10,15}$')
        if not phone or not phone_pattern.match(phone):
            errors.append("Please enter a valid phone number (10-15 digits, can start with +)")
        
        # Validate date and time
        if slot_datetime < datetime.datetime.now():
            errors.append("Please select a future date and time")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Show a spinner while making the API call
            with st.spinner("Creating your booking..."):
                # Create booking through API
                result, status_code = create_booking(name, phone, lesson_type, slot_datetime)
            
            if status_code == 201:  # Created
                st.success("✅ Booking created successfully!")
                
                # Show booking details
                st.subheader("Booking Confirmation")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Booking ID:** {result['booking_id']}")
                    st.markdown(f"**Name:** {result['booking']['name']}")
                    st.markdown(f"**Phone:** {result['booking']['phone']}")
                with col2:
                    st.markdown(f"**Lesson Type:** {result['booking']['lesson_type']}")
                    st.markdown(f"**Date & Time:** {format_datetime(result['booking']['slot_datetime'])}")
                
                # Show confirmation status
                confirmation_status = result.get("confirmation_status", "unknown")
                if confirmation_status == "whatsapp_sent":
                    st.info("✅ A confirmation has been sent to your WhatsApp.")
                elif confirmation_status == "sms_sent":
                    st.info("✅ A confirmation SMS has been sent to your phone.")
                else:
                    st.warning("⚠️ We couldn't send a confirmation message to your phone. Please keep your booking details for reference.")
                
                # Option to view all bookings
                if st.button("View All Bookings"):
                    st.session_state.page = "Dashboard"
                    st.rerun()
            else:
                error_msg = result.get('message', 'Unknown error')
                validation_errors = result.get('validation', {}).get('error_messages', [])
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(error)
                else:
                    st.error(f"Error: {error_msg}")

# Footer
st.markdown("---")
st.markdown("© 2023 RoadMaster Driving School. All rights reserved.") 