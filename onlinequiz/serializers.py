from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['roomId', 'type', 'name', 'members']

class ChatMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'user', 'message', 'timestamp']
