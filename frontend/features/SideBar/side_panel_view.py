import streamlit as st
from features.SideBar import git_helper
from features.SideBar import weather_view
from datetime import datetime

def initialize_session_state() -> None:
    """Initialize session state variables if they don't exist."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'serbia_news' not in st.session_state:
        st.session_state.serbia_news = []


def main():
    weather_view.main()
    initialize_session_state()
    display_current_date()
    # Streamlit button that triggers the processing
    if st.sidebar.button('🎗️Git Daily Commits'):
        git_helper.process_repositories()
   

def display_current_date() -> None:
    """Display the current date in the sidebar."""
    current_date = datetime.now().strftime("%B %d, %Y")
    st.sidebar.info(f"Current Date: {current_date}")