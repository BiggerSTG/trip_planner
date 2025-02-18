from crewai.tools import BaseTool
import requests
from typing import Any, Dict, List
from dotenv import load_dotenv
import os

#--------------------------------#
## API KEYS
#--------------------------------#

load_dotenv()

# Set API Key for OpenWeatherMap
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

#Set API Key for GoogleMAps
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

#-------------------------------#
#-------------------------------#
##          Tools
#-------------------------------#
#-------------------------------#

#-------------------------------#
## Weather Tool
#-------------------------------#

# Define the custom weather tool
class WeatherTool(BaseTool):
    name: str = "Weather Fetcher"  # Add type annotation
    description: str = "Fetches weather data for a list of cities using OpenWeather API."

    def _run(self, cities: List[str]) -> Dict[str, Any]:  # Specify input and output types
        """Fetch weather data for multiple cities."""
        if not isinstance(cities, list):
            return {"Error": "Please provide a list of city names."}

        weather_data = {}
        for city in cities:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data[city] = {
                    "Temperature": f"{data['main']['temp']}°C",
                    "Weather": data["weather"][0]["description"],
                    "Humidity": f"{data['main']['humidity']}%",
                    "Wind Speed": f"{data['wind']['speed']} m/s"
                }
            else:
                weather_data[city] = {"Error": "Could not fetch weather."}

        return weather_data

#-------------------------------#
## Places Tool
#-------------------------------#
class PlacesTool(BaseTool):
    name:str = "Places of Interest Fetcher"
    description: str = "Fetches points of interest for a given location using a Maps API."

    def _run(self, location: str, radius: str, type: str) -> Dict[str, Any]:
        """ Fetch necessary map data for a given location. """
        if not isinstance(location, str):
            return {"Error": "Please provide a valid location."}

        places_info = []
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": location,  # e.g., "41.3851,2.1734" for Barcelona
            "radius": radius,
            "type": type,
            "key": GOOGLE_MAPS_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for result in data.get("results", []):
                name = result.get("name", "N/A")
                rating = result.get("rating", "N/A")
                vicinity = result.get("vicinity", "N/A")
                pricing = result.get("price_level", "N/A")
                opening_hours = result.get("opening_hours", "N/A")
                places_info.append({"name": name, "rating": rating, "vicinity": vicinity, "pricing": pricing, "opening_hours": opening_hours})
        else:
            places_info = {"Error": "Could not fetch places."}

        return places_info