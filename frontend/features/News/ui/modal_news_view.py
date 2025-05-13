import streamlit as st
from services.chat_bot_service import get_chatgpt_response
from features.News.helpers import google_news_api_view

@st.dialog(title="Latest News", width='large')
def display_news_in_modal(search_term):

    with st.spinner(f"Searching current information about {search_term}..."):
        news_articles = google_news_api_view.get_title(search_term)

    st.markdown(f"### 📰 Latest News from {search_term}")
    st.write(f"Found {len(news_articles)} articles.")

    if st.button('Summarize'):
        summarized_news = get_chatgpt_response(
            f"Summarize the following news articles in 10 sentences: {search_term} \n\n"
            f"{' '.join([article.get('title', '') for article in news_articles[0:10]])}"
        )
        split_summarized_news = summarized_news.split('.')
        for i in range(len(split_summarized_news)):
            if len(split_summarized_news[i]) > 0:
                st.markdown(f"#### {i+1}. {split_summarized_news[i]}")
    
    
    if st.button('Show News'):
        filtered_articles = news_articles
        for idx, article in enumerate(filtered_articles):
            with st.container():
                st.markdown("---")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"#### {article.get('title', 'No title')}")
                    st.markdown(f"*Source: {article.get('source', 'Unknown')} • "
                            f"Published: {article.get('published_at', 'No date')}*")
                
                with col2:
                    st.link_button("Read More", article.get('url', '#'), 
                                use_container_width=True)
            
