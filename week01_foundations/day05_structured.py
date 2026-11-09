import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"

class User(BaseModel):
    name: str
    age: int
    city: str = "昆明"

def call_once():
    resp = client.chat.completions.create(
        model="deepseek-chat",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": "编一个用户，以 json 格式返回，字段为 name、age、city，例如：{\"name\": \"张三\", \"age\": 25, \"city\": \"大理\"}"},]
)
    content = resp.choices[0].message.content          
    if content.strip() == "":
        raise Exception("空内容")
    data = json.loads(content)
    user = User.model_validate(data)
    return user


def run_once_with_retry():
    for attempt in range(3):
        try:
            call_once()              # 喊谁，一次尝试
            if attempt == 0:
                return "一次过"
            return "重试过"
        except Exception:
            pass                # 这圈失败了，不处理，循环自己进下一圈
    return "最终失败"

def main():
    tally = {"一次过": 0, "重试过": 0, "最终失败": 0}
    for _ in range(10):
        tally[run_once_with_retry()] += 1
    print(tally)

if __name__ == "__main__":
    main()
