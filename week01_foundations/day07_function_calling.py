# day07_function_calling.py —— Issue #4 手写原生 Function Calling
# 链路：第一轮 create（模型决策）→ 有单子：本地执行 → 回传 → 第二轮 create（模型说人话）
import json
import os
from pathlib import Path
import httpx  # 发网络请求的工具
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"

WEATHER_CODES = {
    0: "晴", 1: "晴", 2: "多云", 3: "阴",
    45: "有雾", 48: "有雾",
    51: "毛毛雨", 53: "毛毛雨", 55: "毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    80: "阵雨", 81: "阵雨", 82: "暴雨",
    95: "雷阵雨",
}

def get_weather(location):
    # 第一步：按城市名查经纬度
    resp1 = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",   # 地名查询接口
        params={"name": location, "count": 1, "language": "zh"},   # 查询条件
    )
    data1 = resp1.json()   # 回包翻译成字典
    if not data1.get("results"):   # 没查到这个城市
        return f"查不到{location}这个城市"   # 返回一句话兜底，别让程序崩
    place = data1["results"][0]   # 篮子第一格：第一个匹配到的城市
    lat = place["latitude"]    # 纬度
    lon = place["longitude"]   # 经度

    # 第二步：按经纬度查实时天气
    resp2 = httpx.get(
        "https://api.open-meteo.com/v1/forecast",   # 天气查询接口
        params={"latitude": lat, "longitude": lon, "current": "temperature_2m,weather_code"},
    )
    current = resp2.json()["current"]   # 当前天气那一格
    temp = current["temperature_2m"]   # 气温
    desc = WEATHER_CODES.get(current["weather_code"], "未知")   # 代码查表翻译
    return f"{desc}，气温 {temp}℃"   # f"..." 是把变量塞进字符串的写法

# 【新增 1】写查询城市人口的工具函数（沿用同一个地理编码接口）
def get_population(location):
    resp = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "zh"},
    )
    data = resp.json()
    if not data.get("results"):
        return f"查不到{location}这个城市"
    
    place = data["results"][0]
    pop = place.get("population")  # 取出人口字段
    if pop is None:
        return f"{location}暂无人口统计数据"
    return f"{place['name']}（{place.get('country', '')}）的人口约为 {pop:,} 人"

# TODO 1：写出 tools 菜单（列表里放一道菜：get_weather，说明书含 name / description / parameters）
tools = [  # 工具菜单
    {
        "type": "function",  # 种类：函数
        "function": {  # 说明书
            "name": "get_weather",  # 工具名
            "description": "获取指定城市的天气信息",  # 用途说明（写给模型看的）
            "parameters": {  # 参数表
                "type": "object",  # 形状：一组格子
                "properties": {  # 格子清单
                    "location": {  # 格子：城市
                        "type": "string",  # 这格填文字
                        "description": "城市名称，例如：杭州"
                    }
                },
                "required": ["location"]  # 必填清单
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_population",
            "description": "获取指定城市的人口信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如：杭州"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def main():
    messages = [{"role": "user", "content": "杭州今天天气怎么样？另外杭州有多少人口？"}]

    resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)  # 发问，接住回包
    message = resp.choices[0].message   # 从篮子掏出那一条消息

    if not message.tool_calls:          # 判断点菜单在不在
        print(message.content)          # 没单子：打印回话内容收工
        return

    messages.append(message)           # 把模型那条消息本尊存进本子

    # 【新增 3】用 for 循环遍历所有单子（防止只取 tool_calls[0] 漏掉第二张单子）
    for tool in message.tool_calls:
        func_name = tool.function.name             # 看单子上点的哪道菜
        args = json.loads(tool.function.arguments) # 取出参数
    
    # 根据名字分发给对应的本地函数执行
        if func_name == "get_weather":
            result = get_weather(args["location"])
        elif func_name == "get_population":
            result = get_population(args["location"])
        else:
            result = f"未知工具：{func_name}"

        # 每执行完一张单子，就对应回传一条 tool 结果（tool_call_id 必须一一对应）
        messages.append({
            "role": "tool",
            "tool_call_id": tool.id,
            "content": result
        })
    resp2 = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)   # 第二轮发问
    print(resp2.choices[0].message.content)   # 打印人话

if __name__ == "__main__":
    main()
