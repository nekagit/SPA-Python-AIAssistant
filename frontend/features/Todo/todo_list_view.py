import streamlit as st
from api import todo_services
from typing import Dict
import pandas as pd

class TodoView:
    """Class to handle todo list display and interactions"""
    
    def __init__(self, todos_df: pd.DataFrame):
        self.todos_df = todos_df
        self.active_todos = todos_df[todos_df['active'] == True] if not todos_df.empty else pd.DataFrame()
        self.completed_todos = todos_df[todos_df['active'] == False] if not todos_df.empty else pd.DataFrame()
        
    def render_empty_state(self):
        """Display a message when no todos exist"""
        st.info("No todos found. Add some tasks to get started!")
    
    def format_todo_display(self, todo: Dict, completed: bool = False) -> str:
        """Format a single todo item for display"""
        todo_color = todo['color']
        label_display = f"[{todo['label']}]" if todo['label'] else ""
        repeat_icon = "🔄 " if todo.get('repeat_daily', False) else ""
        priority_indicator = {"High": "🔴", "Middle": "🟠", "Low": "🟢"}.get(todo['priority'], "")
        
        if completed:
            return f"""
            <div style="
                background-color: #f0f0f0;
                border-left: 5px solid {todo_color};
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 8px;
                opacity: 0.7;
            ">
                <span style="color: {todo_color};">{label_display}</span>
                <span style="text-decoration: line-through;">{todo['name']}</span>
            </div>
            """
        else:
            return f"""
            <div style="
                background-color: {todo_color}33;
                border-left: 5px solid {todo_color};
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 8px;
            ">
                {priority_indicator} {repeat_icon} {todo['name']}
            </div>
            """
    
    def render_active_todos(self):
        """Render the active todos section"""
        st.subheader("Active Tasks")
        
        if self.active_todos.empty:
            st.info("No active tasks. Add some to get started!")
            return
        
        # Get unique labels and add "All" option
        labels = ["All"] + sorted(self.active_todos['label'].unique().tolist())
        selected_label = st.selectbox("Filter by label", labels)
        
        # Filter by selected label
        if selected_label != "All":
            filtered_todos = self.active_todos[self.active_todos['label'] == selected_label]
        else:
            filtered_todos = self.active_todos
        
        # Group by label
        labels_dict = {}
        
        # Handle todos with no label
        for _, todo in filtered_todos.iterrows():
            label = todo['label'] if todo['label'] else "No Label"
            if label not in labels_dict:
                labels_dict[label] = []
            labels_dict[label].append(todo)
        
        # Display todos by label
        for label, todos in sorted(labels_dict.items()):
            with st.expander(f"{label} ({len(todos)})", expanded=True):
                # Sort by priority within each label group
                priority_order = {"High": 0, "Middle": 1, "Low": 2}
                sorted_todos = sorted(todos, key=lambda x: priority_order.get(x['priority'], 3))
                
                for todo in sorted_todos:
                    col_todo, col_actions = st.columns([4, 1])
                    
                    with col_todo:
                        st.markdown(
                            self.format_todo_display(todo),
                            unsafe_allow_html=True
                        )
                    
                    with col_actions:
                        st.write("")  # Add some spacing
                        if st.button("✅", key=f"complete_{todo['id']}"):
                            todo_services.update_todo(todo['id'], {'active': False})
                            st.rerun()
    
    def render_completed_todos(self):
        """Render the completed todos section"""
        st.subheader("Completed Tasks")
        
        if self.completed_todos.empty:
            st.info("No completed tasks yet")
            return
        
        # Add search box for completed items
        search_term = st.text_input("Search completed tasks", "")
        
        # Filter by search term if provided
        filtered_completed = self.completed_todos
        if search_term:
            filtered_completed = filtered_completed[
                filtered_completed['name'].str.contains(search_term, case=False) |
                filtered_completed['label'].str.contains(search_term, case=False, na=False)
            ]
        
        # Add a limit with "Show more" option
        show_all = st.checkbox("Show all completed tasks")
        display_limit = None if show_all else 5
        
        # Display the first few completed todos or all if show_all is checked
        completed_to_show = filtered_completed.iloc[:display_limit] if display_limit else filtered_completed
        
        for _, todo in completed_to_show.iterrows():
            col_todo, col_actions = st.columns([4, 1])
            
            with col_todo:
                st.markdown(
                    self.format_todo_display(todo, completed=True),
                    unsafe_allow_html=True
                )
            
            with col_actions:
                st.write("")  # Add some spacing
                if st.button("↩️", key=f"restore_{todo['id']}"):
                    todo_services.update_todo(todo['id'], {'active': True})
                    st.rerun()
                
                if st.button("🗑️", key=f"delete_done_{todo['id']}"):
                    todo_services.delete_todo(todo['id'])
                    st.rerun()
        
        # Show count of hidden items
        if display_limit and len(filtered_completed) > display_limit:
            st.info(f"{len(filtered_completed) - display_limit} more completed items not shown")
        
        # Add a clear all completed button
        if st.button("Clear All Completed"):
            for _, todo in self.completed_todos.iterrows():
                todo_services.update_todo(todo['id'],  {'active': True})
            st.rerun()
