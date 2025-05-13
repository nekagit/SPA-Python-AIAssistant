import os
import json

def load_file(file_path):
    data = {}
    
    try:
        # Check if file exists
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return {} 
    