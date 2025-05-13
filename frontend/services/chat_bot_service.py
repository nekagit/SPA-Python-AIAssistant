import json
import os
from typing import Dict, List
import requests
import streamlit as st
import google.generativeai as genai
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

frontend_dir = Path(__file__).resolve().parent.parent

# Construct path to .env file
env_path = frontend_dir / '.env'

# Load the environment variables
load_dotenv(env_path)


# Get the API keys from the environment
api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
DIRECTORY_CHAT_BOT_DATA = os.getenv('BASE_DIRECTORY_CHAT_BOT_DAT')

print(api_key)
print(gemini_api_key)
def setup_gemini():
    """Configure the Gemini API"""
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        return True
    return False

def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini about Serbia with web search"""
    try:
        # Initialize Gemini
        model = genai.GenerativeModel('gemini-1.5-pro')
        print('gemini')
        # Create a prompt that includes the current date and instructions
        search_prompt = f""" {prompt}"""
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        }
        
        response = model.generate_content(
            search_prompt,
            safety_settings=safety_settings
        )
        # Add date verification message
        response_text = response.text
        return response_text 
        
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"

def get_chatgpt_response(prompt: str) -> str:
    """Send a prompt to ChatGPT and get the response."""
    client = OpenAI(api_key=api_key)
    
    try:
            # Using chat completions API which is correct for gpt-3.5-turbo
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()

    except Exception as e:
            return f"Error communicating with ChatGPT: {str(e)}"

def initialize_chat_history() -> None:
    """Initialize the chat history in session state if it doesn't exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history() -> None:
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            

def load_saved_prompts(file_path):
    """Reads prompts from a text file, storing them in session state."""
    if "saved_prompts" not in st.session_state:
        st.session_state.saved_prompts = []
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            st.session_state.saved_prompts = [line.strip() for line in f if line.strip()]
    
    return st.session_state.saved_prompts


def get_text_input_chat_respond():
    file_path = os.path.join(DIRECTORY_CHAT_BOT_DATA, 'saved_prompts.txt')
    
    # Initialize session state
    if "saved_prompts" not in st.session_state:
        st.session_state.saved_prompts = []
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = ''
        
    # Load saved prompts
    saved_prompts = load_saved_prompts(file_path)
    
    # Create two columns for input fields
    col1, col2 = st.columns(2)
    
    with col1:
        prompt = st.text_input('How can AI help you?')
    
    with col2:
        saved_prompt = st.selectbox('Choose saved prompt', ["(None)"] + saved_prompts)
    selected_prompts_input = st.text_input('Additional context or parameters')
    submit_chat = st.button('Ask AI', key='ask_ai_button', use_container_width=True)
    
    # Combine prompts and inputs
    if saved_prompt != "(None)":
        # If a saved prompt is selected, combine it with the additional input
        final_prompt = (f"{saved_prompt} {selected_prompts_input}" if selected_prompts_input 
                    else saved_prompt).strip()
    else:
        # If no saved prompt, use the custom prompt
        final_prompt = (f"{prompt} {selected_prompts_input}" if selected_prompts_input 
                    else prompt).strip()
    
    if submit_chat and final_prompt:
        result = get_gemini_response(final_prompt)
        # Add the Q&A to the conversation history
        st.session_state.last_prompt = final_prompt
        st.session_state.brainstorm_text_area += f"\nQ: {final_prompt}\nA: {result}\n"
        st.rerun()
    
    return st.session_state.brainstorm_text_area