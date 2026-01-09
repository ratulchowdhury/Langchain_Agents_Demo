from langchain_openai import ChatOpenAI
from langchain_core.tools import tool 
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchainhub import Client
import requests
from dotenv import load_dotenv

load_dotenv()

hub = Client()

search_tool = DuckDuckGoSearchRun()

@tool
def weather_report(location: str) -> str:
    """Get the current weather report for a given location."""
    weather_api_key = "bc56ff170fd62ea71606e172a2b9d04e"  # Replace with your OpenWeather API key
    url = f'https://api.weatherstack.com/current?access_key={weather_api_key}&query={location}'
    response = requests.get(url)
    data = response.json()
    
    return data

#print("Tool Results", search_tool.run("Latest news on Venezuela Situation"))

llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

# Step 2 (replacement): Pull the React agent from the Hub
prompt = hub.pull("hwchase17/react")
# Step 3 (replacement): Create the agent as a Runnable (no AgentExecutor needed)
tools = [search_tool, weather_report]
agent = create_agent(model=llm, tools=tools, system_prompt= prompt, debug=True)


# Demo run: invoke the agent and print the result

inputs ={"messages":[{"role": "user", "content": "What is the capital of westbengal and what is the weather there?"}]}
for step in agent.stream(inputs, stream_mode="values"):
    message = step["messages"][-1]
    
    if message.type == "human":
        print(f"Input: {message.content}")
    elif message.type == "ai":
        if message.tool_calls:
            if message.content:
                print(f"Agents Thought: {message.content}")
            for tool_call in message.tool_calls:
                print(f"Input Action: {tool_call['name']}")
        else:
            print(f"Final Output: {message.content}")

    elif message.type == "tool":
        print(f"Observation: {message.content}")

print("\n--- Finished chain ---")