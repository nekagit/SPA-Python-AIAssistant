import os
import streamlit as st
from api import git_service
from dotenv import load_dotenv
from pathlib import Path

frontend_dir = Path(__file__).resolve().parent.parent

# Construct path to .env file
env_path = frontend_dir / '.env'

# Load the environment variables
load_dotenv(env_path)

BASE_DIRECTORY = os.getenv('BASE_DIRECTORY')

def get_repository_paths(base_path):
    base_dir = Path(base_path)
    return [d for d in base_dir.iterdir() if d.is_dir()]

def process_repositories():
    base_path = rf"{BASE_DIRECTORY}"
    repositories = get_repository_paths(base_path)
    
    if repositories:
        st.sidebar.write(f"Found {len(repositories)} repositories")
        try:
            git_service.git_daily_commits([repositories])
        except Exception as e:
            st.sidebar.error(f"Error processing {repo_path.name}: {str(e)}")
    else:
        st.sidebar.warning("No repositories found in the specified path")

