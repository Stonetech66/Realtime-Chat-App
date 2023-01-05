from django.urls import re_path
from . import consumers
websocket_urls=[
    re_path(r'ws/group/(?P<group_id>\w+)/$', consumers.GroupConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<username>\w+)/$',consumers.ChatConsumer.as_asgi())
]