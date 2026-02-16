import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()

        # Add to user specific private group
        await self.channel_layer.group_add(f"chat_user_{self.user.id}", self.channel_name)

        # Add to global world group
        await self.channel_layer.group_add("chat_world", self.channel_name)

        # Add to location group
        self.location = self.user.last_location
        await self.channel_layer.group_add(f"chat_loc_{self.location}", self.channel_name)

        # Add to trade group if level >= 4
        if self.user.level >= 4:
            await self.channel_layer.group_add("chat_trade", self.channel_name)

        # Add to clan/alliance groups
        if self.user.clan:
            await self.channel_layer.group_add(f"chat_clan_{self.user.clan}", self.channel_name)
        if self.user.alliance:
            await self.channel_layer.group_add(f"chat_alliance_{self.user.alliance}", self.channel_name)

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(f"chat_user_{self.user.id}", self.channel_name)
            await self.channel_layer.group_discard("chat_world", self.channel_name)
            await self.channel_layer.group_discard(f"chat_loc_{self.location}", self.channel_name)
            if self.user.level >= 4:
                await self.channel_layer.group_discard("chat_trade", self.channel_name)
            if self.user.clan:
                await self.channel_layer.group_discard(f"chat_clan_{self.user.clan}", self.channel_name)
            if self.user.alliance:
                await self.channel_layer.group_discard(f"chat_alliance_{self.user.alliance}", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        channel = data.get('channel', 'world')
        recipient_name = data.get('recipient')

        if not message_text:
            return

        # Backend validation for Trade channel
        if channel == 'trade' and self.user.level < 4:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Торговый чат доступен с 4 уровня.'
            }))
            return

        # Private message handling
        recipient = None
        if channel == 'private' and recipient_name:
            recipient = await self.get_user_by_name(recipient_name)
            if not recipient:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Пользователь {recipient_name} не найден.'
                }))
                return

        # Save message to DB
        msg = await self.save_message(self.user, message_text, channel, self.location if channel == 'location' else None, recipient)

        # Broadcast message
        if channel == 'private' and recipient:
            # Send to recipient
            await self.channel_layer.group_send(
                f"chat_user_{recipient.id}",
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'sender': self.user.username,
                    'channel': channel,
                    'timestamp': msg.created_at.strftime('%H:%M')
                }
            )
            # Also send to sender
            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': message_text,
                'sender': self.user.username,
                'channel': channel,
                'recipient': recipient.username,
                'timestamp': msg.created_at.strftime('%H:%M')
            }))
            return

        group_name = "chat_world"
        if channel == 'location':
            group_name = f"chat_loc_{self.location}"
        elif channel == 'trade':
            group_name = "chat_trade"
        elif channel == 'clan' and self.user.clan:
            group_name = f"chat_clan_{self.user.clan}"
        elif channel == 'alliance' and self.user.alliance:
            group_name = f"chat_alliance_{self.user.alliance}"
        elif channel == 'group':
            group_name = "chat_world" # Fallback

        await self.channel_layer.group_send(
            group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': self.user.username,
                'channel': channel,
                'timestamp': msg.created_at.strftime('%H:%M')
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender'],
            'channel': event['channel'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message(self, user, text, channel, location, recipient=None):
        return ChatMessage.objects.create(
            user=user,
            text=text,
            channel=channel,
            location=location,
            recipient=recipient
        )

    @database_sync_to_async
    def get_user_by_name(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()
        await self.channel_layer.group_add("online_players", self.channel_name)
        await self.broadcast_online_status()

    async def disconnect(self, close_code):
        if hasattr(self, 'user') and self.user.is_authenticated:
            await self.channel_layer.group_discard("online_players", self.channel_name)
            await self.broadcast_online_status()

    async def broadcast_online_status(self):
        await self.channel_layer.group_send(
            "online_players",
            {
                'type': 'online_update'
            }
        )

    async def online_update(self, event):
        online_data = await self.get_online_data()
        await self.send(text_data=json.dumps({
            'type': 'online_list',
            'data': online_data
        }))

    @database_sync_to_async
    def get_online_data(self):
        # Simple implementation: all users are "online" for now
        # In a real app, you'd track active sessions
        users = User.objects.all()
        data = {
            'global': [{'id': u.id, 'username': u.username, 'level': u.level} for u in users],
            'location': [{'id': u.id, 'username': u.username, 'level': u.level} for u in users if u.last_location == self.user.last_location],
            'friends': [],
            'clan': []
        }
        return data
