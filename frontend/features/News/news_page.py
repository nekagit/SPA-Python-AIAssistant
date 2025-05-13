import streamlit as st
import json
import os
from features.News.ui import modal_news_view
from features.News.ui import expander_news_keyword_adder


def load_keywords():
    """Load keywords from JSON file or create default if not exists"""
    file_path = "data/news_keywords.json"
    
    # Create default keywords if file doesn't exist
    if not os.path.exists(file_path):
        default_keywords = [
            {"name": "Serbia", "emoji": "🇷🇸", "search": "Serbia"},
            {"name": "Germany", "emoji": "🇩🇪", "search": "Germany"},
            {"name": "US", "emoji": "🇺🇸", "search": "United States"},
            {"name": "Russia", "emoji": "🇷🇺", "search": "Russia"},
            {"name": "China", "emoji": "🇨🇳", "search": "China"},
            {"name": "World", "emoji": "🌍", "search": "World"},
            {"name": "AI", "emoji": "🤖", "search": "Artificial Intelligence"},
            {"name": "Anime", "emoji": "🎌", "search": "Anime"},
            {"name": "Tech Job", "emoji": "💻", "search": "Technology Jobs"}
        ]
        with open(file_path, 'w') as f:
            json.dump(default_keywords, f, indent=4)
    
    # Load keywords from file
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading keywords: {e}")
        return []


def main():
    st.title('🌐 Global News Dashboard')
    
    if 'keywords' not in st.session_state:
        st.session_state.keywords = load_keywords()
    
    keywords = st.session_state.keywords
    columns_per_row = min(9, len(keywords))
    
    for i in range(0, len(keywords), columns_per_row):
        row_keywords = keywords[i:i+columns_per_row]
        cols = st.columns(columns_per_row)
        
        for j, keyword in enumerate(row_keywords):
            with cols[j]:
                if st.button(f"{keyword['emoji']} {keyword['name']}"):
                    with st.spinner(f"Fetching {keyword['name']} News..."):
                        modal_news_view.display_news_in_modal(search_term=keyword['search'])
    
    expander_news_keyword_adder.news_keyword_adder()
    st.subheader('Custom News Search')
    col11, col12 = st.columns(2, gap='large')

    with col11:
        search_term = st.text_input('Search Term..', value='')

    with col12:
        if st.button("🔍 Search", disabled=not search_term):
            modal_news_view.display_news_in_modal(search_term)
