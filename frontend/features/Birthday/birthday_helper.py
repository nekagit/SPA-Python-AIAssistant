import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from services.file_loader_service import load_file
from datetime import datetime

frontend_dir = Path(__file__).resolve().parent.parent.parent
env_path = frontend_dir / '.env'
load_dotenv(env_path)


def load_birthday_data():
    birthday_data = {}
    try:
        base_dir = Path(os.getenv('BASE_DIRECTORY_PROJECT'))
        file_path = base_dir / 'frontend' / 'features' / 'Birthday' / 'birthdays.json'
        birthday_data = load_file(file_path)
        return birthday_data
    except Exception as e:
        st.error(f"Error loading birthday data: {str(e)}")

def prepare_birthday_events():
    birthday_data = load_birthday_data()
    events = []
    current_year = datetime.now().year
    for month, birthdays in birthday_data.items():
        month_num = month_names[month]
        for birthday in birthdays:
            try:
                date_str = f"{current_year}-{month_num:02d}-{birthday['day']:02d}"
                events.append({
                    "title": f"🎂 {birthday['name']}",
                    "start": date_str,
                    "allDay": True,
                    "backgroundColor": "#FF69B4",
                    "borderColor": "#FF1493"
                })
            except (KeyError, TypeError) as e:
                st.warning(f"Error processing birthday entry: {str(e)}")
                continue

    return events

def get_todays_birthdays():
    birthday_events = prepare_birthday_events()
    today = datetime.now().date()
    todays_birthdays = [
        event for event in birthday_events
        if datetime.strptime(event["start"], "%Y-%m-%d").date() == today
    ]
    st.write(f"Today's Birthdays: {todays_birthdays}")  



month_names = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }