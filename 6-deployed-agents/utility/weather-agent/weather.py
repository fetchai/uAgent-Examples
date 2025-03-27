import os
import requests

from uagents import Model
from uagents.models import Field

API_KEY = os.getenv("WEATHERAPI_KEY")

class WeatherForecastRequest(Model):
    location: str = Field(
        description="Location", 
    )

class WeatherForecastResponse(Model):
    location: str
    temp: float
    condition: str
    humidity: float
    wind_speed: float


async def get_weather(location) -> dict:
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=no"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

    weather_data = response.json()

    if "error" in weather_data:
        return {"error": weather_data["error"]["message"]}

    return {
        "location": location,
        "temp": weather_data["current"]["temp_c"],
        "condition": weather_data["current"]["condition"]["text"],
        "humidity": weather_data["current"]["humidity"],
        "wind_speed": weather_data["current"]["wind_kph"],
    }