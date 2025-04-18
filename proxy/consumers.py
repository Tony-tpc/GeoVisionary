import asyncio
import json
import os
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from email import message_from_string
from time import sleep

import httpx
import websockets
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv
from proxy.websocket_client import preprocess_text, STOP_PUNCTUATIONS

## ChatConsumer 依赖
from users.models import FrontendUser, UserConversation, UserConversationHeader
import uuid
from asgiref.sync import sync_to_async

load_dotenv()
DS_MODEL = os.environ.get("DS_MODEL")
V3_MODEL = os.environ.get("V3_MODEL")
DS_KEY = os.environ.get("DS_KEY")
DS_KEY2 = os.environ.get("DS_KEY2")
TXDT_Key = os.environ.get("TXDT_Key")


class BaseConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isOldchat = ""  # 是否是旧对话
        self.user = None  # 用户实例
        self.msg = ""  # 用户输入
        self.full_content = {"content": "", "reasoning": ""}  #  LLM输出
        self.save_task = None  # 保存对话的异步任务

    async def connect(self):
        print(datetime.now().isoformat())
        await self.accept()

    async def disconnect(self, close_code):
        """WebSocket 断开连接时，取消正在运行的任务"""
        pass

    async def receive(self, text_data):
        """获取user_id 和 messages，判断是否旧对话"""
        data = json.loads(text_data)
        user_id = data.get("user_id")
        task = data.get("task", "response")
        if user_id:
            self.user = await sync_to_async(FrontendUser.objects.get)(user_id=user_id)
        match task:
            case "response":
                model_type = data.get("llm", "ds")
                print(model_type)
                messages = data.get("message", [])
                self.isOldchat = data.get("isOldchat")
                # 如果是新的会话，isOldchat收到null
                # 如果不是，isOldchat收到上一次会话的id
                await self.handle_message(messages)
                # 获取历史链
                history_messages = []
                if self.isOldchat:
                    history_messages = await self.get_full_history_back(self.isOldchat)

                message = history_messages + [{"role": "user", "content": self.msg}]
                return await self.get_llm_config(model_type, message)
            case "get_full_history":
                precursor_id = data.get("precursor_id")
                history = await self.get_full_history_top(precursor_id)
                print("history", history)
                print(datetime.now().isoformat())
                await self.send(
                    text_data=json.dumps(
                        {"history": history, "isOldchat": self.isOldchat}
                    )
                )
                await self.disconnect(200)
            case "get_preview":
                preview = await self.get_preview_history()
                await self.send(text_data=json.dumps({"preview": preview}))
                await self.disconnect(200)

    async def handle_message(self, messages):
        self.msg = messages[0]["content"]

    async def get_llm_config(self, model_type, chat_history):
        """获取 LLM 配置"""
        if model_type == "ds":
            return {
                "url": "https://api.siliconflow.cn/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {DS_KEY}",
                    "Content-Type": "application/json",
                },
                "payload": {
                    "model": V3_MODEL,
                    "messages": chat_history,
                    "stream": True,
                    "max_tokens": 4096,
                    "temperature": 0.6,
                    "top_p": 0.7,
                },
            }
        elif model_type == "dslocal":
            return {
                "url": "https://api.siliconflow.cn/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {DS_KEY}",
                    "Content-Type": "application/json",
                },
                "payload": {
                    "model": DS_MODEL,
                    "messages": chat_history,
                    "stream": True,
                    "max_tokens": 4096,
                    "temperature": 0.6,
                    "top_p": 0.7,
                },
            }
        else:
            return {
                "url": "http://localhost:1234/v1/chat/completions",
                "headers": {"Content-Type": "application/json"},
                "payload": {
                    "model": "deepseek-r1-distill-llama-8b",
                    "messages": chat_history,
                    "max_tokens": 4096,
                    "temperature": 0.6,
                    "stream": True,
                },
            }

    @sync_to_async
    def save_conversation(self, session_id):
        from django.db.utils import IntegrityError
        from django.core.exceptions import ValidationError
        print(self.isOldchat)
        try:
            precursor_id = self.isOldchat if self.isOldchat else uuid.uuid4().hex
            # 不是如果是Oldchat，新建一个前驱等于后继
            # 如果不是newchat，前驱等于前端传入的结点
            UserConversation.objects.create(
                frontend_user=self.user,
                precursor_id=precursor_id,
                session_id=session_id,
                user_message=self.msg,
                llm_response=self.full_content["content"],
            )
            if not self.isOldchat:
                UserConversationHeader.objects.create(
                    frontend_user=self.user,
                    precursor_id=precursor_id,
                    user_message=self.msg,
                    llm_summary=None,
                )
        except IntegrityError as e:
            print("唯一性冲突:", e)
        except ValidationError as e:
            print("字段验证失败:", e.message_dict)
        except Exception as e:
            print("未知错误:", str(e))

    @sync_to_async
    def get_full_history_back(self, current_session_id):
        # try:
        all_sessions = list(
            UserConversation.objects.filter(frontend_user=self.user).order_by(
                "timestamp"
            )
        )
        session_map = {str(s.session_id): s for s in all_sessions}
        history = []
        current = session_map.get(str(current_session_id))  # 类型匹配
        while current:
            history.extend(
                [
                    {"role": "user", "content": current.user_message},
                    {"role": "assistant", "content": current.llm_response},
                ]
            )
            precursor_id = str(current.precursor_id) if current.precursor_id else None
            current = session_map.get(precursor_id) if precursor_id else None

        return history[::-1]  # 按时间正序排列

    async def send_error(self, message):
        await self.send(text_data=json.dumps({"error": message, "completed": True}))
        await self.close()

    @sync_to_async
    def get_full_history_top(self, current_precursor_id):
        # try:
        all_sessions = list(
            UserConversation.objects.filter(frontend_user=self.user).order_by(
                "timestamp"
            )
        )
        session_map = {str(s.precursor_id): s for s in all_sessions}
        history = []
        current = session_map.get(str(current_precursor_id))  # 类型匹配
        while current:
            history.extend(
                [
                    {"role": "user", "content": current.user_message},
                    {"role": "assistant", "content": current.llm_response},
                ]
            )
            session_id = str(current.session_id) if current.session_id else None
            current = session_map.get(session_id) if session_id else None
            self.isOldchat = session_id
        return history  # 按时间正序排列

    @sync_to_async
    def get_preview_history(self):
        # try:
        all_sessions = list(
            UserConversationHeader.objects.filter(frontend_user=self.user).order_by(
                "timestamp"
            )
        )
        result = [
            {
                "precursor_id": str(session.precursor_id),
                "user_msg": session.user_message,
                "timestamp": session.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for session in all_sessions
        ]
        return result


class TTSAudioConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = []
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.stream_task = None  # 存储流式任务
        self.summary_task = None  # 存储摘要任务
        self.error = None  # 存储错误

    async def disconnect(self, close_code):
        """WebSocket 断开连接时，取消正在运行的任务"""
        if self.stream_task and not self.stream_task.done():
            self.stream_task.cancel()
        if self.summary_task and not self.summary_task.done():
            self.summary_task.cancel()

        try:
            await asyncio.gather(
                self.stream_task, self.summary_task, return_exceptions=True
            )
        except asyncio.CancelledError:
            print("任务被主动取消")

    async def receive(self, text_data):
        config = await super().receive(text_data)
        # 并行启动两个任务
        self.summary_task = asyncio.create_task(
            self.request_summary(self.msg)
        )  # 任务 1：生成摘要
        self.stream_task = asyncio.create_task(
            self.stream_and_send(config)
        )  # 任务 2：流式 LLM 响应

        # 同时运行两个任务（不会互相阻塞）
        await asyncio.gather(self.stream_task, self.summary_task)

        # 获取摘要结果
        summary_result = (
            self.summary_task.result() if self.summary_task.done() else None
        )
        if summary_result:
            # 异步发送到 TTS 服务
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "summary",
                        "content": summary_result["text"],
                        "audio": summary_result["audio"],
                    }
                )
            )
            # 发送摘要信息
            asyncio.create_task(self.process_and_send(summary_result["text"]))
        else:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "details": self.error if self.error else "发生未知错误",
                    }
                )
            )

    async def stream_and_send(self, config):
        async for content_chunk in self.stream_llm_response(config):
            await self.send(
                text_data=json.dumps({"type": "text", "content": content_chunk})
            )

    async def stream_llm_response(self, config):
        try:
            print(config)
            print(1)
            async with httpx.AsyncClient() as client:  # 使用异步客户端
                async with client.stream(  # 异步流式请求
                    "POST",
                    config["url"],
                    headers=config["headers"],
                    json=config["payload"],
                ) as response:
                    print(response)
                    if response.status_code != 200:
                        return

                    has_reasoning_started = False
                    has_reasoning_ended = False

                    async for chunk in response.aiter_lines():  # 异步迭代行
                        if chunk.strip() == "data: [DONE]":
                            if has_reasoning_started and not has_reasoning_ended:
                                yield ""
                            yield "[DONE]"
                            break

                        if chunk.startswith("data:"):
                            try:
                                data = json.loads(chunk[5:].strip())
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                content_chunk = ""
                                reasoning = delta.get("reasoning_content", "")
                                content = delta.get("content", "")

                                if "reasoning_content" in delta:
                                    if reasoning:
                                        if not has_reasoning_started:
                                            content_chunk += "<think>"
                                            has_reasoning_started = True
                                        content_chunk += reasoning
                                    if content:
                                        if (
                                            has_reasoning_started
                                            and not has_reasoning_ended
                                        ):
                                            content_chunk += "</think>"
                                            has_reasoning_ended = True
                                        content_chunk += content
                                else:
                                    content_chunk += content

                                if content_chunk:
                                    yield content_chunk
                            except Exception as e:
                                print("解析出错:", e)
        except httpx.TimeoutException:
            self.error = "Request Timeout"
        except httpx.HTTPError as e:
            self.error = f"HTTP Error: {e}"
        except Exception as e:
            self.error = f"Unexpected Error: {e}"

    async def request_summary(self, chat_history):
        # 在最后一条用户输入中加入总结提示词
        summary_prompt = [{
            "role": "system",
            "content": "你是一位经验丰富的高中地理老师，你的学生目前遇到了一些地理问题，你需要耐心地帮助他解决问题，并通俗易懂地讲解。记住，你只能用中文思考和回答。如果他输入的是其他方面的问题，也请像个老师一样耐心教导他。"
        },{
            "role": "user",
            "content": chat_history
            + " 请用不超过100字精简地回答这段内容，并且不要用 markdown 格式。",
        }]

        url_ds = "https://api.siliconflow.cn/v1/chat/completions"
        headers_ds = {
            "Authorization": f"Bearer {DS_KEY}",
            "Content-Type": "application/json",
        }
        payload_ds = {
            "model": f"{V3_MODEL}",
            "messages": summary_prompt,
            "stream": False,  # 不需要流式
            "max_tokens": 100,
            "temperature": 0.6,
            "top_p": 0.7,
        }
        test = False
        if test:
            summary = "经纬度是地球表面位置的坐标系统，经度表示东西位置（0°~180°东/西），以本初子午线为基准；纬度表示南北位置（0°~90°北/南），以赤道为基准。两者结合可精确定位地球上任意地点，常用于导航、地图等领域。"
            print("概要内容:", summary)
            sleep(3)
            # 直接生成音频并发送
            audio_b64 = await self.request_tts(summary)
            if audio_b64:
                await self.send(
                    text_data=json.dumps(
                        {"type": "summary", "content": summary, "audio": audio_b64}
                    )
                )
        else:
            try:
                response = requests.post(url_ds, headers=headers_ds, json=payload_ds)
                if response.status_code == 200:
                    summary = response.json()["choices"][0]["message"]["content"]
                    print("概要内容:", summary)

                    # 直接生成音频并发送
                    audio_b64 = await self.request_tts(summary)
                    if audio_b64:
                        await self.send(
                            text_data=json.dumps(
                                {"type": "summary", "content": summary, "audio": audio_b64}
                            )
                        )
                else:
                    print(f"概括请求失败: {response.status_code} - {response.text}")
                    self.error = str(response.text)

            except Exception as e:
                print(f"概括请求异常: {e}")
                self.error = str(e)

    async def request_tts(self, text):
        TTS_SERVER_URI = "ws://127.0.0.1:8080"
        try:
            async with websockets.connect(
                TTS_SERVER_URI, max_size=2**26, ping_interval=30, ping_timeout=120
            ) as websocket:
                await websocket.send(text)
                audio_data = await websocket.recv()

                if audio_data:
                    # 将 bytes 音频数据转换成 Base64 字符串
                    audio_b64 = base64.b64encode(audio_data).decode("utf-8")
                    return audio_b64
                else:
                    print("❌ 收到空音频数据")
                    self.error = "收到空音频数据"
                    return ""

        except asyncio.TimeoutError:
            print("TTS 请求超时（超过 120 秒未响应）")
            self.error = "TTS 请求超时"
            return ""

        except Exception as e:
            print(f"TTS请求失败: {e}")
            self.error = str(e)
            return ""

    async def process_and_send(self, content):
        # 处理 markdown 格式
        content = preprocess_text(content)
        if not content:
            return

        self.queue.append(content)
        combined = "".join(self.queue)

        # 将文本按停顿标点进行切割
        parts = []
        buffer = ""
        for char in combined:
            buffer += char
            if char in STOP_PUNCTUATIONS:
                parts.append(buffer)
                buffer = ""

        # 如果最后一部分不是空的，说明还有剩余片段
        if buffer:
            parts.append(buffer)

        # 传输完整的句子
        for sentence in parts[:-1]:
            if len(sentence.strip()) >= 5:
                await self.request_tts(sentence)

        # 缓存剩余片段（句子未结束的部分）
        self.queue = [parts[-1]] if parts[-1] else []


class ChatConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = r"""
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

    async def disconnect(self, close_code):
        """WebSocket 断开连接时，取消正在运行的任务"""
        print(datetime.now().isoformat())

        if self.save_task and not self.save_task.done():
            self.save_task.cancel()
        try:
            await asyncio.gather(self.save_task, return_exceptions=True)
        except asyncio.CancelledError:
            print("任务被主动取消")

    def sendTX(self, lat, lng):
        try:
            address = (
                requests.get(
                    f"https://apis.map.qq.com/ws/geocoder/v1?key={TXDT_Key}&location={lat},{lng}"
                )
                .json()
                .get("result", {})
                .get("address_component", {})
            )

            # 黑名单
            components = [
                ("nation", ("", "undefined", "Ocean")),
                ("province", ("", "undefined")),
                ("city", ("", "undefined")),
            ]

            return (
                "  ".join(
                    f"{key}: {address.get(key, '')}"
                    for key, excludes in components
                    if address.get(key, "") not in excludes
                )
                or None
            )
            # 如果全部字段无效返回None

        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            print(f"API请求失败: {e}")
            return None

    async def receive(self, text_data):
        config = await super().receive(text_data)
        await self.stream_llm_response(config)

    async def handle_message(self, messages):
        if type(messages) == dict:
            msg_type = messages.get("type")
            if msg_type == "latlng":
                region = await sync_to_async(self.sendTX)(
                    messages["lat"], messages["lng"]
                )
                if region:
                    self.msg = f"""{self.prompt}
                现在，请告诉我{region}位置的地理信息和人文特点：
                纬度 {messages['lat']}，经度 {messages['lng']}"""
                else:
                    self.msg = f"""{self.prompt}
                现在，请告诉我位置的地理信息和人文特点：
                纬度 {messages['lat']}，经度 {messages['lng']}"""
            elif msg_type == "text":
                self.msg = messages.get("text")
        else:
            await self.send_error("Invalid message format")

    async def stream_llm_response(self, config):
        try:
            print(config)
            async with httpx.AsyncClient() as client:  # 使用异步客户端
                async with client.stream(  # 异步流式请求
                    "POST",
                    config["url"],
                    headers=config["headers"],
                    json=config["payload"],
                ) as response:
                    print(response)
                    if response.status_code != 200:
                        raise httpx.HTTPError(f"状态码异常: {response.status_code}")
                    async for chunk in response.aiter_lines():
                        if chunk.strip() == "data: [DONE]":
                            break
                        if chunk.startswith("data:"):
                            try:
                                data = json.loads(chunk[5:].strip())
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                print(delta)

                                # 处理推理链
                                self.full_content["content"] += (
                                    delta.get("content") or ""
                                )

                                self.full_content["reasoning"] += (
                                    delta.get("reasoning_content") or ""
                                )

                                await self.send(
                                    text_data=json.dumps(
                                        {
                                            "content": (delta.get("content") or ""),
                                            "reasoning": (
                                                delta.get("reasoning_content") or ""
                                            ),
                                            "completed": False,
                                        }
                                    )
                                )

                            except Exception as e:
                                print("解析出错:", e)

                    # 发送完成信号，产生会话id，并保存
                    if self.user:
                        session_id = uuid.uuid4().hex
                    self.save_task = asyncio.create_task(
                        self.save_conversation(session_id)
                    )
                    await asyncio.gather(self.save_task)
                    await self.send(
                        text_data=json.dumps(
                            {"completed": True, "session_id": session_id}
                        )
                    )
                    return

        except httpx.TimeoutException:
            self.error = "Request Timeout"
        except httpx.HTTPError as e:
            self.error = f"HTTP Error: {e}"
        except Exception as e:
            self.error = f"Unexpected Error: {e}"