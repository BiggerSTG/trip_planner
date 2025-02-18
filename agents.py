from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from tools import WeatherTool, PlacesTool
import os
from dotenv import load_dotenv


load_dotenv()


# Use Ollama with CrewAI
llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL"),
    base_url=os.getenv("HOST")
)

#-------------------------------#
#-------------------------------#
##          Agents
#-------------------------------#
#-------------------------------#

#-------------------------------#
## Weather Agent
#-------------------------------#

# Initialize the Weather tool
weather_tool = WeatherTool()

weather_agent = Agent(
    role="Weather Expert",
    goal="Fetch current weather details for a list of cities.",
    backstory="Provides accurate weather updates for spontaneous travel planning.",
    llm=llm,
    tools=[weather_tool],
    allow_delegation=False
)

weather_task = Task(
    description="Retrieve weather details for the following cities: {cities}.",
    expected_output="A weather report listing temperature, humidity, and general conditions for each city.",
    agent=weather_agent
)

#-------------------------------#
## Maps Agent
#-------------------------------#

# Initialize the Weather tool
places_tool = PlacesTool()

map_agent = Agent(
    role="Local Expert",
    goal="""
    Fetch map data including points of interest, tourist attractions, and filter them out based on their reviews and opening hours for a specified location.
    You have to be extremely strict for the categories providied. For example, in the categories if tourist attraction and restaurants are given you provide tourist
    attractions and restaurants strictly and not appartment, gyms etc.
            """,
    backstory="""
    Provides accurate and relevant tourist attraction spots, restaurants, points of interest etc, based on the categories provided, for spontaneous travel planning.
    """,
    llm=llm,
    tools=[places_tool],
    allow_delegation=False
)

map_task = Task(
    description="Retrieve map information including tourist attractions, restaurants, points of interest etc. using the following geolocation (use coordinates directly): {location} strictly within a radius of {radius} meters for the following categories: {categories}.",
    expected_output="A perfectly curated map listing tourist attractions, restaurants, points of interest, and other relevant information for the geolocation.",
    agent=map_agent
)