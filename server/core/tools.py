import requests
import random
import datetime
import re
import os

from dotenv import load_dotenv
load_dotenv()

OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_time():
    """Returns current date/time"""
    return datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")

def get_weather(city: str):
    """Mock weather (same as before)"""
    fake_weather = random.choice(["Sunny", "Cloudy", "Rainy", "Windy"])
    temp = random.randint(20, 35)
    return f"The weather in {city} is {fake_weather} with {temp}°C."

def calculate(expression: str):
    """Safely evaluate math expressions"""
    import math
    try:
        allowed = re.compile(r"^[0-9+\-*/().\s]+$")
        if not allowed.match(expression):
            return "Invalid expression"
        return str(eval(expression))
    except Exception:
        return "Error in calculation"

def get_aqi(city: str):
    """
    Fetch live AQI (Air Quality Index) from OpenWeatherMap.
    Falls back to a mock AQI if API fails.
    """
    try:
        if not OWM_API_KEY:
            raise ValueError("Missing OPENWEATHER_API_KEY")

        # 1️⃣ Get coordinates for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWM_API_KEY}"
        geo_resp = requests.get(geo_url, timeout=5)
        geo_data = geo_resp.json()

        if not geo_data:
            return f"Couldn't find location '{city}'."

        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

        # 2️⃣ Get AQI data
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OWM_API_KEY}"
        aqi_resp = requests.get(aqi_url, timeout=5)
        aqi_data = aqi_resp.json()

        if "list" not in aqi_data or not aqi_data["list"]:
            return f"AQI data not available for {city}."

        aqi_value = aqi_data["list"][0]["main"]["aqi"]

        # Convert AQI index (1-5) → readable text
        levels = {
            1: "Good 😊",
            2: "Fair 🙂",
            3: "Moderate 😐",
            4: "Poor 😷",
            5: "Very Poor ☠️",
        }

        return f"The Air Quality Index (AQI) in {city} is {aqi_value} ({levels.get(aqi_value, 'Unknown')})."

    except Exception as e:
        # Fallback mock value
        mock_aqi = random.randint(50, 200)
        level = "Good" if mock_aqi < 100 else "Unhealthy"
        return f"[Offline mode] The Air Quality Index in {city} is {mock_aqi} ({level})."
