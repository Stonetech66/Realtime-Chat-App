from channels.generic.websocket import WebsocketConsumer
import json
from .models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .serializers import GroupMessageSerializers, ChatMessageSerializer
from .models import ChatMessages, Conversation, Group, GroupMessage
from django.shortcuts import get_object_or_404
from uuid import UUID
from django.middleware import common

# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             return obj.hex
#         return json.JSONEncoder.default(self,obj)

class GroupConsumer(JsonWebsocketConsumer):
    # @classmethod
    # def encode_json(cls, content):
    #     return json.dumps(content, cls=UUIDEncoder)

    def connect(self):
                self.user=self.scope['user']
                print(self.user.is_authenticated)
                self.group_id=self.scope['url_route']['kwargs']['group_id']
                try:
                    self.group=Group.objects.get(id=self.group_id)
                except:
                    self.group=None
                if self.group and self.user:
                    async_to_sync(self.channel_layer.group_add)(self.group_id, self.channel_name)
                    self.accept()
                    group_messages=self.group.message.all()
                    self.send(text_data=json.dumps(GroupMessageSerializers(group_messages, many=True).data))

    def receive_json(self, text_data):
        
        message=text_data['message']
        c=GroupMessage.objects.create(user=self.user, group=self.group, message=message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_id,
            {
                'type': 'group_message',
                'message':GroupMessageSerializers(c).data
            }
        )

    def group_message(self, event):
        self.send(text_data=json.dumps(event))

    def disconnect(self,text_data):
        self.send(text_data=json.dumps({'message':'disconnected'}))
        


class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.user=self.scope['user']
        self.to_user_id=self.scope['url_route']['kwargs']['username']
        try:
            self.to_user=User.objects.get(username=self.to_user_id)
        except:
            self.to_user= None
        if self.to_user and self.user:
            self.chat=f'{self.user.id}-{self.to_user.id}'
            try:
                self.conversation=Conversation.objects.get(name=self.chat)
            except:
                self.conversation=Conversation.objects.create(user=self.user, to_user=self.to_user, name=self.chat)
            async_to_sync(self.channel_layer.group_add)(self.chat, self.channel_name)
            self.accept()
            self.send(text_data=json.dumps(ChatMessageSerializer(self.conversation.messages.all(), many=True).data))

    def receive_json(self, text_data):
        data=text_data['message']
        c=ChatMessages.objects.create(from_user=self.user, to_user=self.to_user, message=data, conversation=self.conversation)
        async_to_sync(self.channel_layer.group_send)(self.chat,
       {'message':ChatMessageSerializer(c).data,
        'type':'send_message'}
       )

    def send_message(self, event):
        self.send(text_data=json.dumps(event['message']))

