import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv(Path(__file__).resolve().parent.parent / ".env")



def call_once():
    client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com",
)

    resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "只回答一个数字，不要其他任何内容：1+1="},
    ],
)
    return resp.choices[0].message.content   # 把结果交出来

start_time = time.time()  # 记录开始时间

for i in range(10):  # 循环次
    print(call_once())  # 喊名字，使用它
    

end_time = time.time()  # 记录结束时间
print(f"执行时间: {end_time - start_time} 秒")
