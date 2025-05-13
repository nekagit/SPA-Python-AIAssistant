import streamlit as st
import json
import os

def save_keywords(keywords):
    """Save keywords to JSON file"""
    try:
        path = os.path.join("features", "News", "data", "news_keywords.json")
        with open(path, 'w') as f:
            json.dump(keywords, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving keywords: {e}")
        return False

def news_keyword_adder():
    """
    Expands the news keyword adder functionality.
    """
     # Add section for adding/managing keywords
    with st.expander("📝 Manage News Keywords"):
        st.subheader("Add New Keyword")
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        
        with col1:
            new_emoji = st.text_input("Emoji", value="🔍", key="new_emoji")
        
        with col2:
            new_name = st.text_input("Display Name", key="new_name")
        
        with col3:
            new_search = st.text_input("Search Term", key="new_search", 
                                    help="What to search for (can be different from display name)")
        
        with col4:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("Add", use_container_width=True):
                if new_name and new_search:
                    st.session_state.keywords.append({
                        "name": new_name,
                        "emoji": new_emoji,
                        "search": new_search
                    })
                    if save_keywords(st.session_state.keywords):
                        st.success(f"Added {new_name}")
                        st.rerun()  # Refresh to show new button
                else:
                    st.warning("Please fill in both name and search term")
        
        # Show existing keywords with delete button
        st.subheader("Current Keywords")
        for i, keyword in enumerate(st.session_state.keywords):
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.text(keyword["emoji"])
            with col2:
                st.text(f"{keyword['name']} → {keyword['search']}")
            with col3:
                if st.button("Delete", key=f"del_{i}", use_container_width=True):
                    st.session_state.keywords.pop(i)
                    save_keywords(st.session_state.keywords)
                    st.rerun()  # Refresh to update the list
    