import websockets
import markdown
from bs4 import BeautifulSoup

STOP_PUNCTUATIONS = {'.', '。', '!', '！', '?', '？', '；', ';', '，', ','}

# 去除文字中所有的 markdown 格式
def preprocess_text(text):
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

# WebSocket客户端
queue = []

# 将 LLM 生成内容送给 CosyVoice
async def send_to_tts(content):
    uri = "ws://localhost:8080"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(content)
            print(f"[TTS] 已发送: {content}")
    except Exception as e:
        print(f"[TTS] 连接失败: {e}")

async def process_and_send(content):
    global queue
    content = preprocess_text(content)
    if not content:
        return

    queue.append(content)
    combined = ''.join(queue)

    # 判断队列是否满足条件
    if len(combined) >= 5 and any(p in combined for p in STOP_PUNCTUATIONS) and combined.count(',') + combined.count('，') <= 1:
        await send_to_tts(combined)
        queue.clear()