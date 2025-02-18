from crewai import Crew
from agents import weather_agent, weather_task, map_agent, map_task
from flask import Flask, request

app = Flask(__name__)

# Create a Crew to execute the task
crew = Crew(
    agents=[weather_agent, map_agent],
    tasks=[weather_task, map_task],
    process="sequential",
    verbose=True
)

# Print the result
print("############")
#print(result)

@app.route('/run', methods=['GET'])
def predict():
    # Execute the crew with input cities
    result = crew.kickoff(
        inputs={"cities": ["New York", "London", "Tokyo"], "location": "33.416151, -111.910912", "radius": 1000,
                "categories": "tourist_attractions"})
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)