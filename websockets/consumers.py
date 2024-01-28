import json
from asgiref.sync import sync_to_async

# 3rd party
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Connections


class Consumer(AsyncWebsocketConsumer):

    @sync_to_async
    def add_connection_to_db(self):
        # map user with channel_name and save it
        Connections.objects.create(
            user=self.scope['user'],
            channel_id=self.channel_name
        )

    @sync_to_async
    def remove_connection_to_db(self):
        try:
            connection_instance = Connections.objects.get(
                user=self.scope['user'],
                channel_id=self.channel_name
            )
            connection_instance.delete()
        except:
            pass

    async def connect(self):
        await self.add_connection_to_db()
        await self.accept()


    async def disconnect(self, code):
        await self.remove_connection_to_db()
        print(f'[DISCONNECT] {code}')


    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'message': text_data}))
    

    async def transaction_update(self, event):
        message = event['message']
        status = message.get('status')

        print(f'[WEBSOCKET] {message}')
        
        str_message = json.dumps(message)
        await self.send(text_data=str_message)

        # close connection if status is 'closed'
        if status == 'closed':
            await self.close()