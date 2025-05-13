import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000/task"
# Fetch all tasks from the backend
def fetch_tasks():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching tasks: {response.status_code}")
    return []

# Fetch task by ID
def fetch_task_by_id(task_id):
    response = requests.get(f"{API_URL}/{task_id}")
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching task {task_id}: {response.status_code}")
    return None

# Create new task
def create_task(task_data):
    try:
        response = requests.post(API_URL, json=task_data)
        response.raise_for_status()  # This will throw an exception for 4xx/5xx errors
        st.success("task created successfully!")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error creating task: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Update task by ID
def update_task(task_id, task_data):
    response = requests.put(f"{API_URL}/{task_id}", json=task_data)
    if response.status_code == 200:
        st.success(f"task {task_id} updated successfully!")
    else:
        st.error(f"Error updating task: {response.status_code} - {response.text}")


# Delete task by ID
def delete_task(task_id):
    response = requests.delete(f"{API_URL}/{task_id}")
    if response.status_code == 200:
        st.success(f"task {task_id} deleted successfully!")
    else:
        st.error(f"Error deleting task: {response.status_code}")
