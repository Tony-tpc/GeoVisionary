"""
ASGI config for GeoVisionary_Backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from GeoVisionary_Backend import routings
from GeoVisionary_Backend.middlewares import StreamingMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GeoVisionary_Backend.settings")

application = ProtocolTypeRouter({
    "http": StreamingMiddleware(get_asgi_application()),  # http 路由
    "websocket": URLRouter(routings.websocket_urlpatterns),  # WebSocket 路由
})
