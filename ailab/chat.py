import requests

def chat_qwen(content: str) -> str:
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model":"Qwen/QwQ-32B",
        "messages":[
            {
                "role":"user",
                "content":content
            }
        ],
        "stream":False,
        "temperature":0.7,
    }
    
    headers = {
        "Authorization": "Bearer sk-idfqlgubpgmgeiynvqkparltzyfvffsgiguxpdfvvtglhpge",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_content = response.json()["choices"][0]["message"]["content"]
    return response_content

if __name__ == "__main__":
    content = input("Please enter your question: ")
    print(chat_qwen(content))