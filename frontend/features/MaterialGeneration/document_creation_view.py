import streamlit as st
from services.file_folder_helper import save_file
import os
from services.chat_bot_service import get_gemini_response
def initialize_session_state():
    if 'document_content_text_area' not in st.session_state:
        st.session_state.document_content_text_area = ""

def main():
    initialize_session_state()
    document = st.file_uploader("Find your document:")
    if document: st.session_state.document_content_text_area = document.getvalue()
    prompt = st.text_input('How can AI help you?', key='document_ai_input')
    submit_chat = st.button('Ask AI', key='ask_ai_button_document', use_container_width=True)
    if submit_chat:
        st.session_state.document_content_text_area = get_gemini_response(f'{prompt} for {st.session_state.document_content_text_area}')
        print(st.session_state.document_content_text_area)
        st.rerun()
    document_content = st.text_area(
            'Document Content',
            value=st.session_state.document_content_text_area,
            height=600,
            key='document_content'
        )
    document_name = st.text_input('Write the document name', value=document.name if document else '')
    document_path = st.text_input('Write the document directory path', value='C:\\Users\\Nenad\\Documents\\AI Generated Material')
    if st.button('Save Document') and document_name and document_path:
        file_path = os.path.join(document_path, document_name)
        save_file(file_path, document_content)