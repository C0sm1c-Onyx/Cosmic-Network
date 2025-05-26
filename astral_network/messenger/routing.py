from django.urls import re_path

from messenger.consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<unique_chat_code>\w+)/$', ChatConsumer.as_asgi()),
]