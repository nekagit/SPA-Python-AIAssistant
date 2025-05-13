import streamlit as st
from services import chat_bot_service

def main():
    st.title("Enhanced Chat Assistant")
    st.caption("Powered by ChatGPT and Gemini")
    chat_bot_service.setup_gemini()
   
    chat_bot_service.initialize_chat_history()
    # Chat input
    checkbox = st.checkbox('ChatGPT')
    if checkbox:
         if prompt := st.chat_input("What would you like to ask?", key='chat_gpt'):
        # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_bot_service.get_chatgpt_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    else:
         if prompt := st.chat_input("What would you like to ask?", key='gemini'):
        # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_bot_service.get_gemini_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    chat_bot_service.display_chat_history()
   