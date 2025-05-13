import streamlit as st

from features.MaterialGeneration import document_creation_view, material_generation

def main():
    st.title('Home Page')
    with st.expander('Document creation'):
        document_creation_view.main()
    with st.expander('Material Generation'):
        material_generation.main()
        