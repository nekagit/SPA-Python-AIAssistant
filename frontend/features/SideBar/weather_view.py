import streamlit as st
import requests
from datetime import datetime
import time

# API Configuration - It's better to use st.secrets in production
API_KEY = '18a18122183c771bee90c258407eb01f'

def get_location():
    """Get user location with better error handling and validation"""
    default_location = {
        'lat': 44.7467,  # Šabac latitude
        'lon': 19.6908,  # Šabac longitude
        'city': 'Šabac',
        'country': 'RS'  # RS is the country code for Serbia
    }
    
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if all(key in data for key in ['latitude', 'longitude', 'city', 'country']):
                return {
                    'lat': float(data['latitude']),
                    'lon': float(data['longitude']),
                    'city': data['city'],
                    'country': data['country']
                }
    except Exception as e:
        st.warning("Could not detect location, using default location (Šabac).")
    
    return default_location

def fetch_weather(lat, lon):
    """Fetch weather data with improved error handling"""
    try:
        # Validate coordinates
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            raise ValueError("Invalid coordinates")

        # Fetch current weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather"
        current_params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric',
            'appid': API_KEY
        }
        
        current_response = requests.get(current_url, params=current_params)
        if current_response.status_code != 200:
            st.error(f"Current weather API error: {current_response.text}")
            return None, None
            
        current_weather = current_response.json()

        # Fetch forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast"
        forecast_params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric',
            'appid': API_KEY
        }
        
        forecast_response = requests.get(forecast_url, params=forecast_params)
        if forecast_response.status_code != 200:
            st.error(f"Forecast API error: {forecast_response.text}")
            return current_weather, None

        forecast_data = forecast_response.json()
        
        if 'list' not in forecast_data or not forecast_data['list']:
            st.warning("No forecast data available")
            return current_weather, None

        # Get tomorrow's forecast
        current_time = datetime.now()
        tomorrow_forecast = None
        
        for forecast in forecast_data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if forecast_time.day != current_time.day:
                tomorrow_forecast = forecast
                break
        
        if not tomorrow_forecast and forecast_data['list']:
            tomorrow_forecast = forecast_data['list'][0]

        return current_weather, tomorrow_forecast

    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None, None

def display_weather_card(weather_data, title="Current Weather"):
    """Display weather information with error handling"""
    if not weather_data:
        st.warning(f"{title} data not available")
        return

    try:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            temp = weather_data.get('main', {}).get('temp')
            feels_like = weather_data.get('main', {}).get('feels_like')
            if temp is not None and feels_like is not None:
                st.metric(
                    "Temperature",
                    f"{round(temp)}°C"
                )
            
        with col2:
            humidity = weather_data.get('main', {}).get('humidity')
            if humidity is not None:
                st.metric("Humidity", f"{humidity}%")
            
        with col3:
            wind_speed = weather_data.get('wind', {}).get('speed')
            if wind_speed is not None:
                st.metric("Wind Speed", f"{round(wind_speed)} m/s")
            
        # Weather description and icon
        weather_info = weather_data.get('weather', [{}])[0]
        if weather_info:
            weather_description = weather_info.get('description', '').capitalize()
            weather_icon = weather_info.get('icon')
            # if weather_icon:
            #     icon_url = f"http://openweathermap.org/img/w/{weather_icon}.png"
            #     st.markdown(
            #         f"<div style='text-align: center'><img src='{icon_url}' style='width: 100px'><br>{weather_description}</div>",
            #         unsafe_allow_html=True
            #     )

    except Exception as e:
        st.error(f"Error displaying weather card: {str(e)}")

def main():
    # Get user's location
    location = get_location()
    
    # Sidebar content
    with st.sidebar:
        if location:
            st.subheader(f"{location['city']}, {location['country']}")
            current_weather, _ = fetch_weather(location['lat'], location['lon'])
            if current_weather:
                display_weather_card(current_weather)
    