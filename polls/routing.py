# mysite/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/lobby/", consumers.ChatConsumer.as_asgi()),
]
