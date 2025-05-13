import streamlit as st
import requests
import pandas as pd
API_URL = "http://127.0.0.1:8000/todo"
# Fetch all todos from the backend
def fetch_todos():
    response = requests.get(API_URL)
    if response.status_code == 200:
        df= pd.DataFrame(response.json())
        return df
    st.error(f"Error fetching todos: {response.status_code}")
    return []

# Fetch todo by ID
def fetch_todo_by_id(todo_id):
    response = requests.get(f"{API_URL}/{todo_id}")
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching todo {todo_id}: {response.status_code}")
    return None

# Create new todo
def create_todo(todo_data):
    try:
        response = requests.post(API_URL, json=todo_data)
        response.raise_for_status()  # This will throw an exception for 4xx/5xx errors
        st.success("todo created successfully!")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error creating todo: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Update todo by ID
def update_todo(todo_id, todo_data):
    response = requests.put(f"{API_URL}/{todo_id}", json=todo_data)
    if response.status_code == 200:
        st.success(f"todo {todo_id} updated successfully!")
    else:
        st.error(f"Error updating todo: {response.status_code} - {response.text}")
    st.rerun()

# Delete todo by ID
def delete_todo(todo_id):
    response = requests.delete(f"{API_URL}/{todo_id}")
    if response.status_code == 200:
        st.success(f"todo {todo_id} deleted successfully!")
    else:
        st.error(f"Error deleting todo: {response.status_code}")
