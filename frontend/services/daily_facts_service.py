from services import chat_bot_service
from datetime import datetime
def get_daily_facts(context):
    # Optimized prompt for daily facts
    today = datetime.now().date()
    prompt = f"""
    Generate a set of brief and interesting daily facts for today’s date {today} for this country {context}. 
    Format your response strictly as a JSON object with the following keys and values (each as a short string):
    - todays_fact
    - river_of_the_day
    - meal_of_the_world
    - person_died_today
    - person_born_today
    - invention_today
    - musician_of_the_day
    - song_of_the_day
    - movie_of_the_day
    - book_of_the_day
    - quote_of_the_day

    Each value should be one to two sentences. Keep all facts relevant to today's historical or cultural context.
    """

    # Example JSON structure for reference or validation
    example_output = {
        "todays_fact": "The Eiffel Tower was officially opened to the public on this day in 1889.",
        "river_of_the_day": "The Nile River in Africa is the longest river in the world, stretching over 6,650 kilometers.",
        "meal_of_the_world": "Pho is a Vietnamese noodle soup consisting of broth, rice noodles, herbs, and meat, usually beef or chicken.",
        "person_died_today": "Bob Marley, the Jamaican reggae legend, died on May 11, 1981.",
        "person_born_today": "Salvador Dalí, Spanish surrealist painter, was born on May 11, 1904.",
        "invention_today": "On May 11, 1949, the Siamese twins telephone system was patented by Frank W. Tinker.",
        "musician_of_the_day": "Freddie Mercury, known for his dynamic stage presence and voice, was the lead vocalist of Queen.",
        "song_of_the_day": "‘Imagine’ by John Lennon, released in 1971, remains one of the most influential songs of all time.",
        "movie_of_the_day": "‘The Matrix’, directed by the Wachowskis, was released in 1999 and revolutionized sci-fi cinema.",
        "book_of_the_day": "‘To Kill a Mockingbird’ by Harper Lee, published in 1960, is a classic of modern American literature.",
        "quote_of_the_day": "‘The only way to do great work is to love what you do.’ — Steve Jobs"
    }
    complete_prompt = f"{prompt}\n\nExample Output:\n{example_output}"
    response = chat_bot_service.get_chatgpt_response(complete_prompt)
    return response, today
