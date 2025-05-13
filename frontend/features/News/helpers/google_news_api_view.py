import sys
from pygooglenews import GoogleNews

def get_title(search):
    gn = GoogleNews(lang='en')  # Use Serbian language
    search_results = gn.search(search)
    
    stories = []
    if 'entries' in search_results:
        for item in search_results['entries']:
            stories.append({'title': item.title, 'link': item.link})
    print(stories)
    return stories
