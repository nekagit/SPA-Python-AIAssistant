from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os
from features.MaterialGeneration.material_service import generate_material
from services.file_folder_helper import load_file_from_path, save_file
frontend_dir = Path(__file__).resolve().parent.parent

# Construct path to .env file
env_path = frontend_dir / '.env'

# Load the environment variables
load_dotenv(env_path)

DIRECTORY_CHAT_BOT_DATA = os.getenv('BASE_DIRECTORY_PROJECT')

def initialize_session_state():
    if 'brainstorm_text_area' not in st.session_state:
        st.session_state.material_content_text_area = ""
    if 'brainstorm_text_area' not in st.session_state:
        st.session_state.prompts_content_text_area = ""

def main():
    initialize_session_state()  # Don't comment this out
    
    base_dir = Path(DIRECTORY_CHAT_BOT_DATA)
    data_material = base_dir / "frontend" / "data" / "chat_bot_data" / 'material' / 'material.txt'
    prompt_material = base_dir / "frontend" / "data" / "chat_bot_data" / 'prompt' / 'prompt.txt'
    
    material_file = str(Path(st.text_input('Directory for Material Saving', value=data_material, key='material_generation')))
    prompts_file = str(Path(st.text_input('Directory for Prompts', value=prompt_material, key='prompts')))
    
    # Create load buttons
    col1_load, col2_load = st.columns([1, 1])
    with col1_load:
        if st.button("Load Material", key="load_material"):
            st.session_state.material_content_text_area = load_file_from_path(material_file)
    with col2_load:
        if st.button("Load Prompts", key="load_prompts"):
            st.session_state.prompts_content_text_area = load_file_from_path(prompts_file)
    
    # Create text areas
    col1, col2 = st.columns([1, 1])
    with col1:
        material_content = st.text_area(
            'Material Content',
            value=st.session_state.material_content_text_area,
            height=600,
            key='material_content'
        )
        if st.button('Save Material'):
            save_file(material_file, material_content)
    
    with col2:
        prompts_content = st.text_area(
            'Prompts Content',
            value=st.session_state.prompts_content_text_area,
            height=600,
            key='prompts_content'
        )
        if st.button('Save Prompt'):
            save_file(prompts_file, prompts_content)  # Fixed: was saving to material_file
    
    if st.button('Generate Material', key='generate_submit'):
        generate_material(material_file, prompts_file)
