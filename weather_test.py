from typing import Any, Dict, List
import requests
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Set API Key for OpenWeatherMap
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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

# Initialize the custom tool
weather_tool = WeatherTool()

# Use Ollama with CrewAI
llm = ChatOpenAI(
    model="ollama/deepseek-r1:14b",
    base_url="http://localhost:11434/"
)

# Create an Agent that fetches weather data
weather_agent = Agent(
    role="Weather Expert",
    goal="Fetch current weather details for a list of cities.",
    backstory="You provide accurate weather updates for users planning their travels or daily schedules.",
    llm=llm,
    tools=[weather_tool],  # Attach the custom weather tool
    allow_delegation=False
)

# Define the weather fetching task
weather_task = Task(
    description="Retrieve weather details for the following cities: {cities}.",
    expected_output="A weather report listing temperature, humidity, and general conditions for each city.",
    agent=weather_agent
)

# Create a Crew to execute the task
crew = Crew(
    agents=[weather_agent],
    tasks=[weather_task],
    process="sequential",
    verbose=True
)

# Execute the crew with input cities
result = crew.kickoff(inputs={"cities": ["New York", "London", "Tokyo"]})

# Print the result
print("############")
print(result)
