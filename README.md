# LangChain Agents Demo

This project demonstrates how to build and run a simple agent using LangChain, OpenAI, and DuckDuckGo Search. The agent is designed to perform web searches and provide summaries based on user queries.

## Prerequisites

- Python 3.12 or higher
- An OpenAI API Key
- A WeatherStack API Key (optional, for weather tool)

## Setup

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment**:
    - Windows:
      ```powershell
      .venv\Scripts\activate
      ```
    - macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    LANGCHAIN_API_KEY=your_langchain_api_key_here # Optional, for tracing
    LANGCHAIN_TRACING_V2=true # Optional
    ```
    Note: The weather tool in `simple_agents_demo.py` may utilize a hardcoded key or require setup. Check the code for `weather_api_key`.

## Usage

Run the agent demo script:

```bash
python simple_agents_demo.py
```

## Description

- **`simple_agents_demo.py`**: The main script that initializes a ReAct agent. It uses `DuckDuckGoSearchRun` for web searches and a custom `weather_report` tool. It processes a user query about Venezuela interactions and prints the agent's thought process, actions, observations, and final output to the console.

## Dependencies

- langchain
- langchain-openai
- langchain-community
- langchainhub
- duckduckgo-search
- python-dotenv
- requests
