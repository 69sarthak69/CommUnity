import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import Room, Message
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room name from the URL and create a unique group name
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Add this connection to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

     # Remove the connection from the group on disconnect
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse incoming message data
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']
        timestamp = data.get('timestamp', datetime.datetime.now().isoformat())

        try:
            sender = await sync_to_async(User.objects.get)(id=sender_id)
            room = await sync_to_async(Room.objects.get)(name=self.room_name)

            await sync_to_async(Message.objects.create)(
                room=room,
                sender=sender,
                content=message
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender_id,
                    'username': sender.username,  # ✅ send username from here
                    'timestamp': timestamp,
                }
            )
        except Exception as e:
            print("❌ Error saving message:", e)

    async def chat_message(self, event):
        # Send broadcast message back to WebSocket
        print("📩 Broadcasting:", event)  # ✅ debug print
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))

