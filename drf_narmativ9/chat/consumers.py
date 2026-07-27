import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'global_chat'

        # Xonaga (Group) qo'shilish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Xonadan chiqish
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # WebSocket'dan xabar kelganda
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        username = data.get('username', 'Anonymous')

        # Xabarni guruhdagi barcha userlarga yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Group'dan xabar kelganda WebSocket'ga uzatish
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))