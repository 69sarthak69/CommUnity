import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"notifications_{self.user_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["notification"]))


class HelpRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.request_id = self.scope['url_route']['kwargs']['request_id']
        self.group_name = f"help_request_{self.request_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

class CommunityFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "community_feed"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("Client connected to community_feed")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_feed_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
