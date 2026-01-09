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

"""

values] {'messages': [HumanMessage(content='What is the capital of westbengal and what is the weather there?', additional_kwargs={}, response_metadata={}, id='36e0c975-af00-4207-ab69-3d48d5df9c0c'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 52, 'prompt_tokens': 326, 'total_tokens': 378, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_deacdd5f6f', 'id': 'chatcmpl-CvzTSpenuFDtWj3vdpxiWq3Qxit1H', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--019ba142-58f0-7a91-9db8-0af90f16ff1e-0', tool_calls=[{'name': 'duckduckgo_search', 'args': {'query': 'capital of West Bengal'}, 'id': 'call_08dVhRbvAnZZsof3GnDfB1qW', 'type': 'tool_call'}, {'name': 'weather_report', 'args': {'location': 'Kolkata'}, 'id': 'call_RzT1jWU8pxIKsNtNJeI4pbio', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 326, 'output_tokens': 52, 'total_tokens': 378, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}
Input Action: duckduckgo_search
Input Action: weather_report
Observation: {"request": {"type": "City", "query": "Kolkata, India", "language": "en", "unit": "m"}, "location": {"name": "Kolkata", "country": "India", "region": "West Bengal", "lat": "22.570", "lon": "88.370", "timezone_id": "Asia/Kolkata", "localtime": "2026-01-09 11:04", "localtime_epoch": 1767956640, "utc_offset": "5.50"}, "current": {"observation_time": "05:34 AM", "temperature": 19, "weather_code": 143, "weather_icons": ["https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0006_mist.png"], "weather_descriptions": ["Haze"], "astro": {"sunrise": "06:18 AM", "sunset": "05:09 PM", "moonrise": "10:59 PM", "moonset": "10:22 AM", "moon_phase": "Waning Gibbous", "moon_illumination": 66}, "air_quality": {"co": "789.85", "no2": "15.35", "o3": "79", "so2": "23.95", "pm2_5": "102.55", "pm10": "104.45", "us-epa-index": "4", "gb-defra-index": "4"}, "wind_speed": 13, "wind_degree": 343, "wind_dir": "NNW", "pressure": 1019, "precip": 0, "humidity": 60, "cloudcover": 0, "feelslike": 19, "uv_index": 6, "visibility": 2, "is_day": "yes"}}
Final Output: The capital of West Bengal is Kolkata.
Final Output: The capital of West Bengal is Kolkata.

The current weather in Kolkata is hazy with a temperature of 19°C. The wind is blowing from the NNW at 13 km/h, and the humidity is at 60%. The visibility is reduced to 2 km due to the haze.

"""