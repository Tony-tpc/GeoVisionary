import json
import os
import base64
import websockets
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv

from proxy.websocket_client import preprocess_text, STOP_PUNCTUATIONS

load_dotenv()
DS_MODEL = os.environ.get("DS_MODEL")
DS_KEY = os.environ.get("DS_KEY")

class TTSAudioConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat_history = data.get('messages', [])
        print(chat_history)

        # 请求 LLM API
        async for content_chunk in self.stream_llm_response(chat_history):
            await self.send(text_data=json.dumps({"type": "text", "content": content_chunk}))
            # 异步发送到 TTS 服务
            await self.process_and_send(content_chunk)

    async def stream_llm_response(self, chat_history):
        url_ds = "https://api.siliconflow.cn/v1/chat/completions"
        headers_ds = {
            "Authorization": f"Bearer {DS_KEY}",
            "Content-Type": "application/json",
        }
        payload_ds = {
            "model":  f"{DS_MODEL}",
            "messages": chat_history,
            "stream": True,
            "max_tokens": 4096,
            "temperature": 0.6,
            "top_p": 0.7,
        }

        response = requests.post(url_ds, headers=headers_ds, json=payload_ds, stream=True)
        if response.status_code != 200:
            return

        has_reasoning_started = False
        has_reasoning_ended = False
        decoder = response.iter_lines()

        for chunk in decoder:
            if not chunk.strip():
                continue

            if chunk == b"data: [DONE]":
                if has_reasoning_started and not has_reasoning_ended:
                    yield ""
                yield "[DONE]"
                break

            if chunk.startswith(b"data:"):
                try:
                    json_data = json.loads(chunk[6:])
                    delta = json_data.get("choices", [{}])[0].get("delta", {})
                    content_chunk = ""
                    reasoning = delta.get("reasoning_content", "")
                    content = delta.get("content", "")
                    key = "reasoning_content"

                    if key in delta:
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

    async def request_tts(self, text):
        TTS_SERVER_URI = "ws://127.0.0.1:8080"
        try:
            async with websockets.connect(TTS_SERVER_URI) as websocket:
                await websocket.send(text)
                audio_data = await websocket.recv()

                if audio_data:
                    # 将 bytes 音频数据转换成 Base64 字符串
                    audio_b64 = base64.b64encode(audio_data).decode("utf-8")
                    await self.send(text_data=json.dumps({
                        "type": "audio",
                        "content": audio_b64
                    }))
                else:
                    print("❌ 收到空音频数据")

        except Exception as e:
            print(f"TTS请求失败: {e}")

    async def process_and_send(self, content):
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