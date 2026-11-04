import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI
import time

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com",
)


async def call_once(i):
    try:
        resp = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": "只回答一个数字，不要其他任何内容：1+1="},
            ],
        )
    except Exception:
        return f"第{i}个请求失败"
    return resp.choices[0].message.content   # 把结果交出来

async def main():
    tasks = [call_once(i) for i in range(10)]  # 先造：10 张待办单（这是 for 的紧凑写法，叫列表推导式）
    start = time.time()
    results = await asyncio.gather(*tasks)     # 后等：* 是把列表拆开一张张递给 gather
    print(f"并行耗时: {time.time() - start:.2f} 秒")
    print(results)                             # 应该看到 10 个 "2" 整齐排列
asyncio.run(main())