from pathlib import Path
import streamlit as st
import os
from services import chat_bot_service
from services.file_folder_helper import save_file, load_file_from_path
from dotenv import load_dotenv

frontend_dir = Path(__file__).resolve().parent.parent

# Construct path to .env file
env_path = frontend_dir / '.env'

# Load the environment variables
load_dotenv(env_path)


DIRECTORY_CHAT_BOT_DATA = os.getenv('BASE_DIRECTORY_PROJECT')

def initialize_session_state():
    if 'brainstorm_text_area' not in st.session_state:
        st.session_state.brainstorm_text_area = ""

def main():
    initialize_session_state()
    
    base_dir = Path(DIRECTORY_CHAT_BOT_DATA)
    savee_dir = base_dir / "frontend" / "data" / "chat_bot_data"
    save_dir = str(Path(st.text_input('Directory for text save', value=savee_dir)))
    
    st.subheader('Text Editor with Save Function')
    chat_bot_service.get_text_input_chat_respond()
    # Use session state for text content
    text_content = st.text_area(
        '',
        value=st.session_state.brainstorm_text_area,
        height=600,
        key='text_content'
    )
    
    # Update session state when text area changes
    st.session_state.brainstorm_text_area = text_content
    
    # File name input with default value
    default_filename = f'{st.session_state.last_prompt}.txt' if st.session_state.last_prompt != '' else 'text.txt' 
    file_name = st.text_input("File name:", value=default_filename)
    
    # Save button
    if st.button("Save Text"):
        try:
            # Full path for the file
            file_path = os.path.join(save_dir, file_name)
            
            # Check if file already exists
            if os.path.exists(file_path):
                col1, col2 = st.columns(2)
                with col1:
                    st.warning(f"File {file_name} already exists.")
                with col2:
                    if st.button("Overwrite"):
                        save_file(file_path, text_content)
            else:
                save_file(file_path, text_content)
            
        except Exception as e:
            st.error(f"An error occurred while saving: {str(e)}")
    
    # Display list of saved files
    st.subheader("Previously Saved Files:")
    if os.path.exists(save_dir):
        saved_files = os.listdir(save_dir)
        if saved_files:
            for file in saved_files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(file)
                with col2:
                    # Load button for each file
                        file_path = os.path.join(save_dir, file)
                        st.session_state.brainstorm_text_area = load_file_from_path(file_path)
        else:
            st.write("No saved files yet.")
    else:
        st.write("Save directory does not exist.")

