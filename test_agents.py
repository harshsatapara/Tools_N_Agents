from langchain_community.tools import tool,Tool
from ddgs import DDGS
import requests
from dotenv import load_dotenv
load_dotenv()
#search_tool = DuckDuckGoSearchRun()
@tool
def search_tool(query: str) -> str:
    """DuckDuckGoSearchRun module to search any query over web and provide the response back."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        if not results:
            return "No results found."
        return "\n\n".join(
            f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}"
            for r in results
        )

@tool
def get_weather_details(city:str) -> dict:
    """This tool will provide weather details for provided city"""
    url = f"https://api.weatherstack.com/current?access_key=feee5677743b3ec5bd0b402ffe792c92&query={city}"
    result = requests.get(url)
    
    return result.json()
    
# search_tool = Tool(
#     name="duckduckgo_search",
#     func=ddgs_search,
#     description="Useful for searching the web for current information."
# )

#search_tool = GoogleSerperAPIWrapper()

#search_result = search_tool.invoke('Top 5 latest news from India')

#print(search_result)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

#llm_result = llm.invoke('hi')

#print(llm_result.content)

from langchain.agents import create_react_agent,AgentExecutor
from langchain import hub

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm=llm,tools=[search_tool,get_weather_details],prompt=prompt)

agent_executor = AgentExecutor(agent=agent,tools=[search_tool,get_weather_details],verbose=True)

result = agent_executor.invoke({"input": "What is the capital of Japan and its current weather condition. Do I need to take my raincoat with me today?"})

print(result)
