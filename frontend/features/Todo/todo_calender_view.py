import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from pathlib import Path

frontend_dir = Path(__file__).resolve().parent.parent

# Construct path to .env file
env_path = frontend_dir / '.env'

# Load the environment variables
load_dotenv(env_path)

BASE_DIRECTORY = os.getenv('BASE_DIRECTORY')

def load_birthday_data():
    # Initialize with empty default data
    birthday_data = {}
    
    try:
        base_dir = Path(os.getenv('BASE_DIRECTORY_PROJECT'))
        file_path = base_dir / 'frontend' / 'data' / 'todo.json'
        
        # Create directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as file:
                birthday_data = json.load(file)
    except Exception as e:
        st.warning(f"Error loading birthday data: {str(e)}")
        birthday_data = {}  # Ensure we have a default value
    events = []
    current_year = datetime.now().year
    
    month_names = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    
    # Only process if we have valid data
    if birthday_data:
        for month, birthdays in birthday_data.items():
            if month in month_names:  # Add safety check for month names
                month_num = month_names[month]
                for birthday in birthdays:
                    try:
                        date_str = f"{current_year}-{month_num:02d}-{birthday['day']:02d}"
                        events.append({
                            "title": f"🎂 {birthday['name']}",
                            "start": birthday['start'],
                            "end": birthday['end'],
                            "start": date_str,
                            "allDay": True,
                            "backgroundColor": "#FF69B4",
                            "borderColor": "#FF1493"
                        })
                    except (KeyError, TypeError) as e:
                        st.warning(f"Error processing birthday entry: {str(e)}")
                        continue
    
    return events

def main():
    st.subheader("Todo Calendar 🎉")
    
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,dayGridWeek,dayGridDay"
        },
        "initialView": "dayGridMonth",
        "selectable": True,
        "editable": False,
        "dayMaxEvents": True,
        "displayEventTime": False,
    }
    
    custom_css = """
        .fc-event-title {
            font-weight: bold;
            font-size: 0.9em;
            padding: 2px;
        }
        .fc-day-today {
            background-color: #f0f8ff !important;
        }
        .fc-toolbar-title {
            font-size: 1.5em !important;
            color: #333;
        }
        .fc-event {
            cursor: pointer;
            margin: 2px 0;
        }
    """
    
    events = load_birthday_data()
    
    calendar_view = calendar(
        events=events,
        options=calendar_options,
        custom_css=custom_css,
        key='todo_calendar'
    )
    
    st.write(calendar_view)