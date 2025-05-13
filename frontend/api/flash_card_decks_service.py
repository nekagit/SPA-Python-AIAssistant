import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/flash_card_deck"
# Fetch all flash_card_decks from the backend
def fetch_flash_card_decks():
    response = requests.get(API_URL)
    if response.status_code == 200:
        df= pd.DataFrame(response.json())
        return df
    st.error(f"Error fetching flash_card_decks: {response.status_code}")
    return []

# Fetch flash_card_deck by ID
def fetch_flash_card_deck_by_id(flash_card_deck_id):
    response = requests.get(f"{API_URL}/{flash_card_deck_id}")
    if response.status_code == 200:
        return response.json()
    st.error(f"Error fetching flash_card_deck {flash_card_deck_id}: {response.status_code}")
    return None

# Create new flash_card_deck
def create_flash_card_deck(flash_card_deck_data):
    try:
        response = requests.post(API_URL, json=flash_card_deck_data)
        print(response)
        response.raise_for_status()  # This will throw an exception for 4xx/5xx errors
        st.success("flash_card_deck created successfully!")
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Error creating flash_card_deck: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# Update flash_card_deck by ID
def update_flash_card_deck(flash_card_deck_id, flash_card_deck_data):
    response = requests.put(f"{API_URL}/{flash_card_deck_id}", json=flash_card_deck_data)
    if response.status_code == 200:
        st.success(f"flash_card_deck {flash_card_deck_id} updated successfully!")
    else:
        st.error(f"Error updating flash_card_deck: {response.status_code} - {response.text}")


# Delete flash_card_deck by ID
def delete_flash_card_deck(flash_card_deck_id):
    response = requests.delete(f"{API_URL}/{flash_card_deck_id}")
    if response.status_code == 200:
        st.success(f"flash_card_deck {flash_card_deck_id} deleted successfully!")
    else:
        st.error(f"Error deleting flash_card_deck: {response.status_code}")
    st.rerun()