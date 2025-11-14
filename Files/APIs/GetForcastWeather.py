# GetForcastWeather.py
# Gets the Weather Forcast for today 
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025


from datetime import datetime
import requests
import json
from dateutil import parser
import os 


def GetForcast():
    WEATHER_ENABLED = os.getenv("FEATURE_WEATHER")
    if (WEATHER_ENABLED != "ENABLED"):
        return
    
    LATITUDE = os.getenv("OPENWEATHERMAP_LATITUDE")
    LONGITUDE = os.getenv("OPENWEATHERMAP_LONGITUDE")
    API_KEY = os.getenv("OPENWEATHERMAP_KEY")
    
    if (LATITUDE == None or LONGITUDE == None or API_KEY == None):
        raise ValueError("Weather Feature Enabled However missing required information")
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&units=metric&appid={API_KEY}"
    response = requests.get(url).json()
    
    weather = "Unknown"
    temperature = None
    icon = None
    try:
        weather = response["weather"][0]["main"]
        temperature = response["main"]["temp"]
        icon = response["weather"][0]["icon"]
    except KeyError as e:
        print(f"Error fetching weather data: {e}")
            
    return [weather, temperature, icon]

if __name__ == "__main__":
    forcastData = GetForcast()
    print(forcastData)

