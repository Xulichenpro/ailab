import os
import getpass
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

os.environ["GOOGLE_API_KEY"] = getpass.getpass("Please enter gemini api key:")
print("password entered")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@tool
def magic_function(input:int) -> int:
    """Applies a magic function to an input."""
    return input + 2

tools = [magic_function]

query = "what is the value of magic_function(3)?"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": query})

from langgraph.prebuilt import create_react_agent

langgraph_agent_executor = create_react_agent(model, tools)


messages = langgraph_agent_executor.invoke({"messages": [("human", query)]})

result = {
            "input": query,
            "output": messages["messages"][-1].content,
        }
print(result)