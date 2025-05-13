import streamlit as st
from streamlit_calendar import calendar
from features.Birthday.birthday_helper import prepare_birthday_events

if 'birthday_calendar_loaded' not in st.session_state:
    st.session_state.birthday_calendar_loaded = False

def birthday_page():
    st.title("Birthday Calendar")
    
    # Force rerun only on first load
    if not st.session_state.birthday_calendar_loaded:
        st.session_state.birthday_calendar_loaded = True
        st.rerun()
    
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
    
    events = prepare_birthday_events()
    
    # Show debug information
    st.write(f"Found {len(events)} birthday events")
    
    # Add a manual refresh button
    if st.button("Refresh Calendar Data"):
        st.rerun()
    
    # Use try-except to handle possible rendering issues
    try:
        calendar(
            events=events,
            options=calendar_options,
            custom_css=custom_css,
            key='birthday_calendar'
        )
    except Exception as e:
        st.error(f"Error rendering calendar: {str(e)}")
        if st.button("Reload Calendar"):
            st.rerun()
