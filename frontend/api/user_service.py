import requests
import streamlit as st
API_URL = "http://127.0.0.1:8000/user"
# Fetch all users from the backend
def fetch_users():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching users: {response.status_code}")
    return []

# Fetch user by ID
def fetch_user_by_id(user_id):
    response = requests.get(f"{API_URL}/{user_id}")
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching user {user_id}: {response.status_code}")
    return None

# Create new user
def create_user(user_data):
    try:
        response = requests.post(API_URL, json=user_data)
        response.raise_for_status()  # This will throw an exception for 4xx/5xx errors
        st.success("user created successfully!")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error creating user: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Update user by ID
def update_user(user_id, user_data):
    response = requests.put(f"{API_URL}/{user_id}", json=user_data)
    if response.status_code == 200:
        st.success(f"user {user_id} updated successfully!")
    else:
        st.error(f"Error updating user: {response.status_code} - {response.text}")


# Delete user by ID
def delete_user(user_id):
    response = requests.delete(f"{API_URL}/{user_id}")
    if response.status_code == 200:
        st.success(f"user {user_id} deleted successfully!")
    else:
        st.error(f"Error deleting user: {response.status_code}")
