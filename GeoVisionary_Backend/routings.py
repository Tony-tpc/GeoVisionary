from django.urls import re_path
from proxy.consumers import TTSAudioConsumer

websocket_urlpatterns = [
    re_path(r"ws/tts/$", TTSAudioConsumer.as_asgi()),
]