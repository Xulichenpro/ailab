import os
import getpass
if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = getpass.getpass("Please enter gemini api key:")

from google import genai

client = genai.Client()

# 2. 定义 Prompt
prompt = "introduce kimi no na wa"

# 3. 调用模型
# 我们使用 'gemini-2.5-flash' 模型，它速度快且性能好
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

# 4. 打印结果
print("Gemini 的回复：")
print(response.text)