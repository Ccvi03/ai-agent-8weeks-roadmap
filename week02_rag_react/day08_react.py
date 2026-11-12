# day08_react.py —— Week 2 Day 8 手写 ReAct（起手骨架：关掉讲解例，自己填 TODO）
# 练手题：杭州今天比北京暖和多少度？（查两次 + 算一次）
import json
import os
from pathlib import Path
import httpx  # 发网络请求的工具
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"
MAX_STEPS = 5  # 保险刹车上限（已定：5 圈）

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
    # 已给：和 day07 一模一样，不用动
    resp1 = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "zh"},
    )
    data1 = resp1.json()
    if not data1.get("results"):
        return f"查不到{location}这个城市"
    place = data1["results"][0]
    lat = place["latitude"]
    lon = place["longitude"]
    resp2 = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current": "temperature_2m,weather_code"},
    )
    current = resp2.json()["current"]
    temp = current["temperature_2m"]
    desc = WEATHER_CODES.get(current["weather_code"], "未知")
    return f"{desc}，气温 {temp}℃"

# TODO 1：写 calculate(a, b, operation) 函数本体
#   - 吃：两个数字 a、b + 一种运算 operation（文字）；吐：一句字符串
#     （返回值记得转成 str —— 回传的 content 必须是文本）
#   - 运算种类你自己定，最少留 subtract（算温差要用）；add / multiply / divide 加不加你定
#   - 除法记得防 b == 0
#   - 最后留一句兜底：不认识的运算 → 返回一句错误说明，别让程序崩
def calculate(a, b, operation):
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        if b == 0:
            return "错误：除数不能为零"
        return str(a / b)
    else:
        return f"错误：不支持的运算 '{operation}'"


tools = [  # 工具菜单
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
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
        },
    },
    # TODO 2：仿照上面那道菜，给 calculate 写说明书，放进这个列表里
    #   - 还是 name / description / parameters 三样
    #   - parameters 有三格：a（number）、b（number）、operation（string，还要带 enum 可选值清单）
    #   - enum 里写哪几个词，必须和 TODO 1 函数里能接住的词一一对上，多一个少一个都会出事
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行基本数学运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number","description": "第一个数字"},
                    "b": {"type": "number","description": "第二个数字"},
                    "operation": {
                        "type": "string",
                        "description": "运算类型",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    }
                },
                "required": ["a", "b", "operation"]
            }
        }
    }
    
]

# TODO 3：写 run_tool(func_name, args) 分发函数
#   - 吃：单子上的名字 + 参数字典；吐：执行结果那句话
#   - 按 func_name 分派到 get_weather 或 calculate，参数从 args 里按格掏
#   - 最后留兜底：不认识的名字 → 返回一句"未知工具：……"
def run_tool(func_name, args):
    if func_name == "get_weather":
        location = args.get("location")
        return get_weather(location)
    elif func_name == "calculate":
        a = args.get("a")
        b = args.get("b")
        operation = args.get("operation")
        return calculate(a, b, operation)
    else:
        return f"未知工具：{func_name}"

# TODO 4：写循环主体（这一章的核心，提示都在下面，代码你自己排）
    #   - 先备两样：计数器 steps = 0、旗子 finished = False
    #   - while 圈顶过保险刹车（steps 和 MAX_STEPS 比）；一进圈先 steps += 1
    #   - 发问 create → 掏 message → 没点单 = 正常刹车：打印答案、把旗子改成 True、break
    #   - 点了单：先 append(message) 存模型这条，再 for 遍历这一圈的每张单：
    #       参数文本先 json.loads → try 里用 run_tool 执行 → except 里把报错包成 result
    #       → append 一条 tool 消息（tool_call_id 填这张单的 id）
    #   - 循环外：if not finished → 打印认输那句（转满上限没答出来）
    #   - 验收小抄：把"打印本子"的那几行加在 create 之前，能亲眼看本子每圈多什么

def main():
    messages = [{"role": "user", "content": "杭州今天比北京暖和多少度？"}]
    steps = 0
    finished = False
    
    while steps < MAX_STEPS:
        steps += 1
        response = client.chat.completions.create(model=MODEL,messages=messages,tools=tools)
        message = response.choices[0].message

        if not message.tool_calls:
            print(message.content)
            finished = True
            break

        messages.append(message)
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            try:
                result = run_tool(tool_name, tool_args)
            except Exception as e:
                result = f"工具执行出错：{str(e)}"
            
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })

if __name__ == "__main__":
    main()
