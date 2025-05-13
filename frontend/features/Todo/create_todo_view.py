import streamlit as st
from api import todo_services


def create_todo_view():
    todo_name = st.text_input('What needs to be done?')
    todo_priority = st.selectbox('Priority', ('Low', 'Middle', 'High'))
    todo_repeat_daily = st.checkbox('Repeats Daily')
    color = st.color_picker('Pick A color', '#00f900')
    label = st.text_input('Label')
    if st.button('Add Task'):
        todo_services.create_todo({
            'name':todo_name,
            'priority': todo_priority,
            'active': True,
            'repeat_daily': todo_repeat_daily,
            'color': color,
            'label': label
            
        })
        st.rerun()  
