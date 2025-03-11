import asyncio
import json
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import httpx
import websockets
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv

from proxy.websocket_client import preprocess_text, STOP_PUNCTUATIONS

load_dotenv()
DS_MODEL = os.environ.get("DS_MODEL")
V3_MODEL = os.environ.get("V3_MODEL")
DS_KEY = os.environ.get("DS_KEY")
DS_KEY2 = os.environ.get("DS_KEY2")

class TTSAudioConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = []
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.stream_task = None  # 存储流式任务
        self.summary_task = None  # 存储摘要任务
        self.error = None # 存储错误

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        """ WebSocket 断开连接时，取消正在运行的任务 """
        if self.stream_task and not self.stream_task.done():
            self.stream_task.cancel()
        if self.summary_task and not self.summary_task.done():
            self.summary_task.cancel()

        try:
            await asyncio.gather(self.stream_task, self.summary_task, return_exceptions=True)
        except asyncio.CancelledError:
            print("任务被主动取消")

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat_history = data.get('messages', [])
        model_type = data.get('llm', 'ds')

        # 并行启动两个任务
        self.summary_task = asyncio.create_task(self.request_summary(chat_history))  # 任务 1：生成摘要
        config = await self.get_llm_config(model_type, chat_history)
        self.stream_task = asyncio.create_task(self.stream_and_send(config))  # 任务 2：流式 LLM 响应

        # 同时运行两个任务（不会互相阻塞）
        await asyncio.gather(self.stream_task, self.summary_task)

        # 获取摘要结果
        summary_result = self.summary_task.result() if self.summary_task.done() else None
        if summary_result:
            # 异步发送到 TTS 服务
            await self.send(text_data=json.dumps(
                {"type": "summary", "content": summary_result["text"], "audio": summary_result["audio"]}))
            # 发送摘要信息
            asyncio.create_task(self.process_and_send(summary_result["text"]))
        else:
            await self.send(text_data=json.dumps(
                {"type": "error","details": self.error if self.error else "发生未知错误"}))

        if self.error:
            await self.send(text_data=json.dumps(
                {"type": "error", "details": self.error}
            ))

    async def stream_and_send(self, config):
        async for content_chunk in self.stream_llm_response(config):
            await self.send(text_data=json.dumps({"type": "text", "content": content_chunk}))

    async def stream_llm_response(self, config):
        try:
            async with httpx.AsyncClient() as client:  # 使用异步客户端
                async with client.stream(  # 异步流式请求
                        'POST',
                        config['url'],
                        headers=config['headers'],
                        json=config['payload'],
                ) as response:
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
                                        if has_reasoning_started and not has_reasoning_ended:
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

    async def get_llm_config(self, model_type, chat_history):
        """获取 LLM 配置"""
        if model_type == "ds":
            return {
                'url': "https://api.siliconflow.cn/v1/chat/completions",
                'headers': {
                    "Authorization": f"Bearer {DS_KEY}",
                    "Content-Type": "application/json",
                },
                'payload': {
                "model": DS_MODEL,
                    "messages": chat_history,
                    "stream": True,
                    "max_tokens": 4096,
                    "temperature": 0.6,
                    "top_p": 0.7,
                }
            }
        else:
            return {
                'url': "http://localhost:1234/v1/chat/completions",
                'headers': {"Content-Type": "application/json"},
                'payload': {
                    "model": "deepseek-r1-distill-llama-8b",
                    "messages": chat_history,
                    "max_tokens": 4096,
                    "temperature": 0.6,
                    "stream": True,
                }
            }

    async def request_summary(self, chat_history):
        # 在最后一条用户输入中加入总结提示词
        summary_prompt = chat_history[:-1] + [
            {
                "role": "user",
                "content": chat_history[-1]["content"] + " 请用不超过100字精简地回答这段内容，并且不要用 markdown 格式。"
            }
        ]

        url_ds = "https://api.siliconflow.cn/v1/chat/completions"
        headers_ds = {
            "Authorization": f"Bearer {DS_KEY2}",
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

        try:
            response = requests.post(url_ds, headers=headers_ds, json=payload_ds)
            if response.status_code == 200:
                summary = response.json()["choices"][0]["message"]["content"]
                print("概要内容:", summary)

                # 直接生成音频并发送
                audio_b64 = await self.request_tts(summary)
                if audio_b64:
                    await self.send(text_data=json.dumps({
                        "type": "summary",
                        "content": summary,
                        "audio": audio_b64
                    }))
            else:
                print(f"概括请求失败: {response.status_code} - {response.text}")
                self.error = str(response.text)

        except Exception as e:
            print(f"概括请求异常: {e}")
            self.error = str(e)

    async def request_tts(self, text):
        TTS_SERVER_URI = "ws://127.0.0.1:8080"
        try:
            async with websockets.connect(TTS_SERVER_URI, max_size=2**26, ping_interval=30, ping_timeout=120) as websocket:
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
            self.error = "语音生成请求超时"
            return ""

        except Exception as e:
            print(f"TTS请求失败: {e}")
            self.error = "语音生成请求失败"
            return ""

    async def process_and_send(self, content):
        # 处理 markdown 格式
        content = preprocess_text(content)
        if not content:
            return

        self.queue.append(content)
        combined = ''.join(self.queue)

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