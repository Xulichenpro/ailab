import requests
import json

api_url = "http://127.0.0.1:5000/calculate"

available_tool = [
{
    "type":"function",
    "function":{
        "name":"calculator",
        "description": "A calculator that can perform basic arithmetic operations such as addition, subtraction, multiplication, and division. Input is a mathematical expression containing two numbers and one operator (+, -, *, /).",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression containing two numbers and one operator (+, -, *, /). For example: '3 + 5', '10 / 2', '7 * 4', '9 - 1'."
                }
            },
            "required": ["expression"]
        }   
    }
    
}]

def chat_qwen_with_tool(content: str) -> str:
    url = "https://api.siliconflow.cn/v1/chat/completions"
    messages = [{"role":"user","content":content}]
    global available_tool
    payload = {
        "model":"Qwen/QwQ-32B",
        "messages":messages,
        "stream":False,
        "temperature":0.7,
        "tools": available_tool,
    }
    
    headers = {
        "Authorization": "Bearer sk-idfqlgubpgmgeiynvqkparltzyfvffsgiguxpdfvvtglhpge",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    print(response)
    tool_calls = response["choices"][0]["message"]["tool_calls"]

    if not tool_calls:
        return response["choices"][0]["message"]["content"]
    else:
        for tool in tool_calls:
            name = tool["function"]["name"]
            args = json.loads(tool["function"]["arguments"])
            if name == "calculator":
                result = requests.get(api_url,params={"expression":args["expression"]}).json()["result"]
                print(result)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool["id"], # 需要工具调用的 ID
                    "name": name,
                    "content": "i used the calculator and got the result."+str(result) # 工具执行结果
                })
                payload = {
                    "model":"Qwen/QwQ-32B",
                    "messages":messages,
                    "stream":False,
                    "temperature":0.7,
                    "tools": available_tool,
                }
                final_response = requests.post(url=url,json=payload,headers=headers).json()
                print(final_response["choices"][0]["message"]["content"])
                return final_response["choices"][0]["message"]["content"]
    
    return "do not get result from qwen"

if __name__ == "__main__":
    content = "what is 12345*54321"
    #content = input("Please enter your question: ")
    chat_qwen_with_tool(content)