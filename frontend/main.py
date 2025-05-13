import streamlit as st
from features.Birthday import birthday_page
from features.ChatBot import chatbot_page
from features.Home import home_page
from features.MaterialGeneration import material_generation_page
from features.News import news_page
from features.Todo import todo_page
from features.SideBar import side_panel_view
from features.Birthday import birthday_helper
from services import daily_facts_service
import json


def home_page_view():
    st.title("Pomaze bog gospodine!")
    st.subheader("Slava ocu i sinu i svetome duhu!")
    birthday_helper.get_todays_birthdays()

    today_facts_country = st.text_input("Which contextual facts would you like to know about? (e.g., country, city, etc.)", "Serbia")
    if st.button('Get Daily Facts'):
        daily_facts, today = daily_facts_service.get_daily_facts(today_facts_country)
        data = json.loads(daily_facts)
        st.write(f"### Daily Facts {today}")
        st.write(f"📘 **Today's Fact**: {data['todays_fact']}")
        st.write(f"🌊 **River of the Day**: {data['river_of_the_day']}")
        st.write(f"🍽️ **Meal of the World**: {data['meal_of_the_world']}")
        st.write(f"🕯️ **Famous Person Who Died Today**: {data['person_died_today']}")
        st.write(f"🎉 **Famous Person Born Today**: {data['person_born_today']}")
        st.write(f"💡 **Famous Invention Today**: {data['invention_today']}")
        st.write(f"🎼 **Musician of the Day**: {data['musician_of_the_day']}")
        st.write(f"🎵 **Song of the Day**: {data['song_of_the_day']}")
        st.write(f"🎬 **Movie of the Day**: {data['movie_of_the_day']}")
        st.write(f"📖 **Book of the Day**: {data['book_of_the_day']}")
        st.write(f"💬 **Quote of the Day**: {data['quote_of_the_day']}")


def main():
    hp, news, todo,  bdc, mg, chatbot = st.tabs(['HomePage', 'News', 'Todo',  'Birthdays', 'Material Generation', 'Chatbot'])
    side_panel_view.main()

    with hp:
        home_page.main()
        home_page_view()
    with news:
        news_page.main()
    with todo:
        todo_page.main()
    with bdc:
        birthday_page.birthday_page()
    with mg:
        material_generation_page.main()   
    with chatbot:
        chatbot_page.main()

    