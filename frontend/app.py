
import streamlit as st

# Set page to wide mode
st.set_page_config(
    page_title="AI Assistant",
    layout="wide",  # This makes the content use more horizontal space
    initial_sidebar_state="expanded"
)

from main import main

if __name__ == "__main__":
    main()