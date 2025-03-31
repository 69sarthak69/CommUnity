# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth.models import AnonymousUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Create room if it doesn't exist
        await self.get_or_create_room()

        await self.send(text_data=json.dumps({
            'message': '👋 Connected to WebSocket!',
            'room': self.room_name
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        if self.user and not isinstance(self.user, AnonymousUser):
            await self.save_message(self.user, message)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'user': self.user.username if self.user else 'Anonymous'
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))

    @database_sync_to_async
    def get_or_create_room(self):
        ChatRoom.objects.get_or_create(name=self.room_name)

    @database_sync_to_async
    def save_message(self, user, content):
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(room=room, user=user, content=content)
