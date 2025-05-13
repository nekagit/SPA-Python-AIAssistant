import streamlit as st
from api import todo_services
import pandas as pd

from features.Todo.todo_list_view import TodoView
from features.Todo.todo_table_view import TodoTable


def display_stats(todos_df: pd.DataFrame):
    """Display statistics about todos"""
    if todos_df.empty:
        return
    
    st.subheader("Task Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    # Count active and completed tasks
    active_count = len(todos_df[todos_df['active'] == True])
    completed_count = len(todos_df[todos_df['active'] == False])
    daily_count = len(todos_df[todos_df['repeat_daily'] == True])
    
    with col1:
        st.metric("Active Tasks", active_count)
    
    with col2:
        st.metric("Completed Tasks", completed_count)
    
    with col3:
        st.metric("Daily Tasks", daily_count)
    
    # Priority distribution
    if not todos_df.empty:
        priority_counts = todos_df[todos_df['active'] == True]['priority'].value_counts()
        labels = priority_counts.index.tolist()
        values = priority_counts.values.tolist()
        
        # Only show chart if there are active tasks
        if sum(values) > 0:
            st.bar_chart(priority_counts)


def display_todo_app():
    """Main function to display the todo app"""
    st.title("Todo App")
    
    # Fetch todos
    todos_df = todo_services.fetch_todos()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(['List View', 'Tasks', 'Statistics'])
    
    # List view tab
    with tab1:
        if todos_df.empty:
            st.info("No todos found. Add some tasks to get started!")
        else:
            view = TodoView(todos_df)
            col1, col2 = st.columns([3, 2])
            
            with col1:
                view.render_active_todos()
            
            with col2:
                view.render_completed_todos()
    
    # Table views
    with tab2:
        table = TodoTable(todos_df)
        table.render_table('Active')
    
    with tab3:
        display_stats(todos_df)


