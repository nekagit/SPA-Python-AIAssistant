import os
from pathlib import Path
import streamlit as st

def save_file(file_path, content):
    if file_path is "" or None:
        file_path = st.file_uploader("Find your document:")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    st.success(f"File saved successfully at: {os.path.abspath(file_path)}")
    
    # Add a download button for the saved file
    with open(file_path, 'r', encoding='utf-8') as f:
        st.download_button(
            label="Download saved file",
            data=f.read(),
            file_name=os.path.basename(file_path),
            mime="text/plain"
        )

def get_content_of_file(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
        

def save_content_to_file(base_dir, filename, content):
    try:
        # Create the base directory if it doesn't exist
        base_dir.mkdir(parents=True, exist_ok=True)
        
        # Create file path without creating an extra directory
        file_path = base_dir / f'{filename}.md'
        
        # Convert to Windows long path format if necessary
        if os.name == 'nt' and len(str(file_path)) > 260:
            file_path = Path('\\\\?\\' + str(file_path.resolve()))
        
        # Write content to file
        file_path.write_text(content, encoding='utf-8')
        print(f"Successfully saved file: {file_path}")
        
    except Exception as e:
        print(f"Error saving file {filename}: {str(e)}")
        raise


def sanitize_filename(filename):
    # Replace any character that's not alphanumeric, dash, or underscore
    sanitized = "".join(c if c.isalnum() else "_" for c in filename)
    return sanitized.strip('_')  # Remove leading/trailing underscores

def truncate_filename(filename, max_length=100):
    if len(filename) <= max_length:
        return filename
    
    # Preserve the file extension if present
    name, ext = os.path.splitext(filename)
    # Leave room for the extension
    max_name_length = max_length - len(ext)
    return name[:max_name_length] + ext

def load_file_from_path(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return ""
    
