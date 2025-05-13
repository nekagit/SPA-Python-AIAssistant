import streamlit as st
from features.Crew.components import crew_api_view, task_api_view

def show_crew_ai():
    st.title("Streamlit Frontend for FastAPI")

    # Define tabs
    tab2, tab3, tab4 = st.tabs(["User", "Crew", "Task"])

    with tab2:
        crew_api_view.show_crew_api_view()

    with tab3:
        task_api_view.show_task_api_view()
        
    with tab4:
        task_api_view.show_task_api_view()