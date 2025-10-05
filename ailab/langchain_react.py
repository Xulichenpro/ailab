import os
import getpass
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

os.environ["GOOGLE_API_KEY"] = getpass.getpass("Please enter gemini api key:")
print("password entered")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@tool
def magic_function(input:int) -> int:
    """Applies a magic function to an input."""
    return input + 2

tools = [magic_function]

query = "what is the value of magic_function(3)?"

memory = MemorySaver()

system_message = "You are a helpful assistant."

langgraph_agent_executor = create_react_agent(model, tools, checkpointer=memory,prompt=system_message)

config = {"configurable": {"thread_id": "test-thread","checkpoint_ns":"chat_history"}}
print(
    langgraph_agent_executor.invoke(
        {
            "messages": [
                ("user", "Hi, I'm polly! What's the output of magic_function of 3?")
            ]
        },
        config,
    )["messages"][-1].content
)
print("---")
print(
    langgraph_agent_executor.invoke(
        {"messages": [("user", "Remember my name?")]}, config
    )["messages"][-1].content
)
print("---")
print(
    langgraph_agent_executor.invoke(
        {"messages": [("user", "what was that output again?")]}, config
    )["messages"][-1].content
)