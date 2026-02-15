import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BattleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'battle_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'chat':
            await self.channel_layer.group_send(
                'global_chat',
                {
                    'type': 'chat_message',
                    'message': data['text'],
                    'sender': self.user_id
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'text': event['message'],
            'from': event['sender']
        }))
