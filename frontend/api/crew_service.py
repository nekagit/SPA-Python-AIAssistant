import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000/crew"
API_URL2 = "http://127.0.0.1:8000/crew"
# Fetch all crews from the backend
def fetch_crews():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching crews: {response.status_code}")
    return []

# Fetch crew by ID
def fetch_crew_by_id(crew_id):
    response = requests.get(f"{API_URL}/{crew_id}")
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching crew {crew_id}: {response.status_code}")
    return None

# Create new crew
def create_crew(crew_data):
    try:
        response = requests.post(API_URL, json=crew_data)
        response.raise_for_status()  # This will throw an exception for 4xx/5xx errors
        st.success("crew created successfully!")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error creating crew: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Update crew by ID
def update_crew(crew_id, crew_data):
    response = requests.put(f"{API_URL}/{crew_id}", json=crew_data)
    if response.status_code == 200:
        st.success(f"crew {crew_id} updated successfully!")
    else:
        st.error(f"Error updating crew: {response.status_code} - {response.text}")


# Delete crew by ID
def delete_crew(crew_id):
    response = requests.delete(f"{API_URL}/{crew_id}")
    if response.status_code == 200:
        st.success(f"crew {crew_id} deleted successfully!")
    else:
        st.error(f"Error deleting crew: {response.status_code}")
