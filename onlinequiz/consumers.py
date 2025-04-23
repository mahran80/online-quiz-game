import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # جلب userId من الرابط
        self.user_id = self.scope['url_route']['kwargs']['userId']
        self.user = await database_sync_to_async(User.objects.get)(id=self.user_id)
        
        # جلب كل الغرف اللي المستخدم مشترك فيها
        self.rooms = await database_sync_to_async(list)(
            ChatRoom.objects.filter(members=self.user)
        )

        # إضافة المستخدم لكل الغرف
        for room in self.rooms:
            await self.channel_layer.group_add(
                room.roomId,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        # إزالة المستخدم من الغرف عند الخروج
        for room in self.rooms:
            await self.channel_layer.group_discard(
                room.roomId,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        room_id = data.get('roomId')
        message = data.get('message')

        if action == 'message':
            chat = await database_sync_to_async(ChatRoom.objects.get)(roomId=room_id)
            chat_message = await database_sync_to_async(ChatMessage.objects.create)(
                chat=chat, user=self.user, message=message
            )
            await self.channel_layer.group_send(
                room_id,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
