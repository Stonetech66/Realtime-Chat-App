from rest_framework import serializers
from .models import GroupMessage, Group, ChatMessages

class UserSerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    username=serializers.CharField(read_only=True)

class GroupMessageSerializers(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    user=UserSerializer(read_only=True)
    message=serializers.CharField(read_only=True)
    date_created=serializers.DateTimeField(read_only=True)

class GroupDetailSerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    name=serializers.CharField(read_only=True)
    description=serializers.CharField(read_only=True)
    members=UserSerializer(many=True, read_only=True)
    online=serializers.IntegerField(read_only=True, source='get_total_online')

class GroupListSerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    name=serializers.CharField(read_only=True)
    description=serializers.CharField(read_only=True)
    members=serializers.IntegerField(read_only=True, source='total_members')
    online=serializers.IntegerField(read_only=True, source='get_total_online')


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['name','description']

class GroupMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupMessage
        fields=[ 
            'message'
        ]
class MessageSerializer(serializers.Serializer):
    message=serializers.CharField(read_only=True)
    last_chatted=serializers.DateTimeField(read_only=True, source='date')

class ChatMessageSerializer(serializers.Serializer):
    to_user=UserSerializer(read_only=True)
    message=serializers.CharField(read_only=True)
    date=serializers.DateTimeField(read_only=True)


        
class ChatHistorySerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    to_user=UserSerializer(read_only=True)
    message=serializers.SerializerMethodField()

    def get_message(self, obj):
        return MessageSerializer(obj.messages.last()).data



