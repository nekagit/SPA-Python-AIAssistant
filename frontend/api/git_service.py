import os
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/git" 

def git_daily_commits(directories):
    try:
        # Validate directories path
        if not directories:
            st.error("No directories provided")
            return
        
        # Make the API call
        response = requests.get(API_URL+'/daily_commits', params={'directories': directories})
        response.raise_for_status()  
        
        # Parse and display the response
        results = response.json()
        for result in results:
            if result.get('returncode') == 0:
                st.success("git_daily_commits executed successfully!")
            else:
                st.error(f"Command failed with return code {result.get('returncode')}")
            st.rerun()

    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")