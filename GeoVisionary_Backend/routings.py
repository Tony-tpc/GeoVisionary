from django.urls import re_path
from proxy.consumers import TTSAudioConsumer, ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/tts/$", TTSAudioConsumer.as_asgi()),
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
]