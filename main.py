from crewai import Crew
from agents import weather_agent, weather_task, map_agent, map_task

# Create a Crew to execute the task
crew = Crew(
    agents=[weather_agent, map_agent],
    tasks=[weather_task, map_task],
    process="sequential",
    verbose=True
)

# Execute the crew with input cities
result = crew.kickoff(inputs={"cities": ["New York", "London", "Tokyo"], "location": "33.416151, -111.910912", "radius": 1000, "categories": "tourist_attractions"})

# Print the result
print("############")
print(result)