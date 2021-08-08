import json

from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            self.room = await self.get_or_create_room()

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            messages = await self.get_previous_messages()

            await self.send(text_data=json.dumps({
                'type': 'previous_messages',
                'messages': messages
            }))

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_or_create_room(self):
        obj, created = ChatRoom.objects.get_or_create(room_name=self.room_name)
        return obj

    @database_sync_to_async
    def get_message_object(self, message_id):
        message = Message.objects.filter(id=message_id)
        return serializers.serialize('json', message)

    @database_sync_to_async
    def get_previous_messages(self):
        messages_qs = Message.objects.filter(chat_room=self.room.id)
        return serializers.serialize('json', messages_qs)
