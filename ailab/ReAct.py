import os
import getpass
from magic_tools import magic_tool_1,magic_tool_2,magic_tools
from google.genai import types
from google import genai

default_system_message = """
    You are a helpful ReAct agent.
    You must follow the format below in every response:
    Thought: Describe what you are thinking or reasoning about the problem.
    Action: If you need to use a tool, call it using function_call.
    Observation: When you receive tool output, use it to continue reasoning.
    Answer: Give the final answer to the user when ready.

    Rules:
    - Always think step by step before answering.
    - If you need a tool, only use one function_call at a time.
    - Do NOT skip Thought or Action sections.
"""

class react_agent:
    def __init__(self,system_message:str = default_system_message,tools:list[dict] = None):
        self.messages = [
            types.Content(
                role = "user",
                parts = [types.Part(text= system_message)]
            )
        ]
        self.client = genai.Client()
        self.tools = tools

        tools = types.Tool(function_declarations=tools)
        self.config = types.GenerateContentConfig(tools=[tools])

    def chat(self,query:str) -> str:
        self.messages.append(
            types.Content(
                role = "user",parts = [types.Part(text=query)]
            )
        )

        response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=self.messages,
                    config=self.config,
                )
        
        while response.candidates[0].content.parts[0].function_call:
            for part in response.candidates[0].content.parts:
                if part.text:
                    print(part.text)  
                if part.function_call:
                    print("Function Call:", part.function_call)
            tool = response.candidates[0].content.parts[0].function_call   
            name = tool.name
            args = tool.args
            args = ", ".join(f"{key}={val}" for key, val in args.items())
            result = eval(name + "(" + args + ")")
            function_response_part = types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
            self.messages.append(response.candidates[0].content) 
            self.messages.append(types.Content(role="user", parts=[function_response_part])) 

            response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=self.messages,
                    config=self.config,
                )
        
        print(response.text)
        return response.text
    
    def clear(self):
        if len(self.messages) > 1:
            del self.messages[1:len(self.messages)]

if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        os.environ["GEMINI_API_KEY"] = getpass.getpass("Please enter gemini api key:")
    agent = react_agent(tools= magic_tools)
    query = "Hi,I'm James.WHat is the value of magic_tool_1(magic_tool_2(2))?"
    agent.chat(query)
    query = "What is my name ?"
    agent.chat(query)