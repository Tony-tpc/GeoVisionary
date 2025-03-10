from django.http import StreamingHttpResponse
from django.http import JsonResponse
import json
import requests
import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view

load_dotenv()
DS_MODEL = os.environ.get("DS_MODEL")
print(DS_MODEL)
DS_KEY = os.environ.get("DS_KEY")
TXDT_Key = os.environ.get("TXDT_Key")

prompt = r"""
请按照以下格式回答：

1. **地理位置**：
   - 经纬度：{纬度}, {经度}
   - 所属国家/地区：{国家/地区}
   - 所属省份/州：{省份/州}
   - 所属城市：{城市}

2. **地理信息**：
   - 地形：{地形类型}
   - 气候：{气候类型}
   - 自然资源：{自然资源}

3. **人文特点**：
   - 人口：{人口数量}
   - 语言：{主要语言}
   - 文化特色：{文化特色}
   - 著名景点：{著名景点}

4. **其他信息**：
   - 历史背景：{历史背景}
   - 经济发展：{经济发展}
"""

def sendTX(lat, lng):
    try:
        address = (
            requests.get(f"https://apis.map.qq.com/ws/geocoder/v1?key={TXDT_Key}&location={lat},{lng}")
            .json()
            .get("result", {})
            .get("address_component", {})
        )

        # 黑名单
        components = [
            ("nation", ("", "undefined", "Ocean")),
            ("province", ("", "undefined")),
            ("city", ("", "undefined"))
        ]

        return "  ".join(
            f"{key}: {address.get(key, '')}"
            for key, excludes in components
            if address.get(key, "") not in excludes
        ) or None  
        # 如果全部字段无效返回None

    except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
        print(f"API请求失败: {e}")
        return None



@api_view(['POST'])
def chat_completion(request):
    try:
        # 解析前端请求数据
        body_data = json.loads(request.body)
        user_message = body_data.get("message", "")
        if type(user_message) == dict:
            match user_message["type"]:  # 类型判断
                case "latlng":

                    region = sendTX(user_message["lat"], user_message["lng"])
                    if region:
                        msg = f"""{prompt}
现在，请告诉我{region}位置的地理信息和人文特点：
纬度 {user_message['lat']}，经度 {user_message['lng']}"""
                    else:
                        msg = f"""{prompt}
现在，请告诉我位置的地理信息和人文特点：
纬度 {user_message['lat']}，经度 {user_message['lng']}"""
                case "text":
                    msg = user_message["text"]
        history = body_data.get("history", [])
        print(msg)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    print(msg)
    # 配置外部API请求参数
    # 未加history
    url_ds = "https://api.siliconflow.cn/v1/chat/completions"
    headers_ds = {
        "Authorization": f"Bearer {DS_KEY}",
        "Content-Type": "application/json",
    }
    payload_ds = {
        "model": f"{DS_MODEL}",
        "messages": [{"role": "user", "content": msg}],
        "stream": True,
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.7,
        # 其他参数...
    }

    def generate():
        try:
            # 请求外部API并获取流式响应
            response = requests.post(
                url_ds, json=payload_ds, headers=headers_ds, stream=True
            )
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]  # 去除'data: '前缀

                        if data_str == "[DONE]":
                            # 流结束标志
                            yield json.dumps({"completed": True}).encode() + b"\n"
                            break
                        try:
                            data = json.loads(data_str)
                            print(data["choices"][0]["delta"])
                            chunk_data = (
                                json.dumps(
                                    {
                                        "content": data["choices"][0]["delta"].get(
                                            "content", None
                                        ),
                                        "reasoning": data["choices"][0]["delta"].get(
                                            "reasoning_content", None
                                        ),
                                        "completed": False,
                                    }
                                )
                                + "\n"
                            )
                            print(chunk_data)
                            yield chunk_data.encode("utf-8")
                        except json.JSONDecodeError as e:
                            print(f"JSON解析错误: {e}")
            # 确保发送完成标志
            yield json.dumps({"completed": True}).encode() + b"\n"
        except Exception as e:
            # 错误处理
            error_chunk = json.dumps({"error": str(e)}) + "\n"
            yield error_chunk.encode("utf-8")

    # 返回流式响应，设置内容类型为ndjson
    return StreamingHttpResponse(generate(), content_type="application/x-ndjson")