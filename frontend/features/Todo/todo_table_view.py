import streamlit as st
from api import todo_services
import pandas as pd


class TodoTable:
    """Class to handle tabular view of todos"""
    
    def __init__(self, todos_df: pd.DataFrame):
        self.todos_df = todos_df
    
    def get_filtered_todos(self, mode: str) -> pd.DataFrame:
        """Filter todos based on the selected mode"""
        filtered_df = self.todos_df.sort_values(by="id", ascending=True)
        
        if mode == 'Active':
            return filtered_df[filtered_df['active'] == True]
        elif mode == 'Not Active':
            return filtered_df[filtered_df['active'] == False]
        elif mode == 'Daily':
            return filtered_df[filtered_df['repeat_daily'] == True]
        return filtered_df
    
    def render_table(self, mode: str):
        """Render an editable table of todos"""
        filtered_df = self.get_filtered_todos(mode)
        
        if filtered_df.empty:
            st.info(f"No {mode.lower()} tasks found")
            return
        
        # Add the delete column
        filtered_df = filtered_df.copy()
        filtered_df['Delete'] = False
        
        # Configure the data editor
        edited_df = st.data_editor(
            filtered_df,
            hide_index=True,
            disabled=["id", "name", "priority"],  # Make other columns read-only
            key=f"todo_table_{mode}"
        )
        
        # Handle changes
        if edited_df is not None:
            # Handle deletions
            to_delete = edited_df[edited_df['Delete'] == True]
            if not to_delete.empty:
                for _, row in to_delete.iterrows():
                    todo_services.delete_todo(row['id'])
                st.success(f"Deleted {len(to_delete)} task(s)")
                st.rerun()
            
            # Handle other updates
            for index, row in edited_df.iterrows():
                updates = {}
                original_row = filtered_df.loc[filtered_df['id'] == row['id']].iloc[0]
                
                # Check which fields have changed
                if row['active'] != original_row['active']:
                    updates['active'] = row['active']
                
                if row['repeat_daily'] != original_row['repeat_daily']:
                    updates['repeat_daily'] = row['repeat_daily']
                
                if row['label'] != original_row['label']:
                    updates['label'] = row['label']
                
                if row['color'] != original_row['color']:
                    updates['color'] = row['color']
                
                # Apply updates if there are any
                if updates:
                    todo_services.update_todo(row['id'], updates)
                    st.success(f"Updated task: {row['name']}")
                    st.rerun()

