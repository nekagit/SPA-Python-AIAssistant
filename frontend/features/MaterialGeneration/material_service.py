import os
import streamlit as st
from services.chat_bot_service import get_chatgpt_response
from services.file_folder_helper import get_content_of_file, sanitize_filename,save_content_to_file, truncate_filename 
from pathlib import Path
from dotenv import load_dotenv

frontend_dir = Path(__file__).resolve().parent.parent

env_path = frontend_dir / '.env'

load_dotenv(env_path)

material_directory = str(Path(os.getenv('BASE_MATERIAL_SAVE_DIRECTORY')))


def generate_material(material_file, prompts_file):
    st.session_state.material_list = get_content_of_file(material_file)
    st.session_state.prompt_list = get_content_of_file(prompts_file)
    
    for material in st.session_state.material_list:
        material_safe = sanitize_filename(material)
        current_material_folder = Path(material_directory) / material
        st.session_state.previous_list_output = ''
        
        for prompt in st.session_state.prompt_list:
            prompt_word, prompt_command = prompt.split(';')
            content = get_chatgpt_response(f'{prompt_command} For this topic {material}')
            
            if prompt_word == 'List':
                st.session_state.previous_list_output = content
                save_content_to_file(current_material_folder, f'{prompt_word}_{material_safe}', content)
                
            elif prompt_word == 'Handout':
                handout_folder = current_material_folder / f'{material}_Handouts'
                for toc_entry in st.session_state.previous_list_output.split('\n'):
                    if not toc_entry.strip():  # Skip empty lines
                        continue
                    toc_entry_safe = sanitize_filename(toc_entry)
                    handout_content = get_chatgpt_response(f'{prompt_command} {toc_entry}')
                    # Truncate filename if too long
                    safe_filename = truncate_filename(f'{material}_{prompt_word}_{toc_entry_safe}')
                    save_content_to_file(handout_folder, safe_filename, handout_content)
            
            else:
                save_content_to_file(current_material_folder, f'{prompt_word}_{material_safe}', content)
