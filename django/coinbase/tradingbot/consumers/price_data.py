from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PricesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Add the consumer to the 'prices_group' group
        await self.channel_layer.group_add(
            'prices_group',  # Group name
            self.channel_name  # Channel name
        )

    async def disconnect(self, close_code):
        # Remove the consumer from the 'prices_group' group
        await self.channel_layer.group_discard(
            'prices_group',  # Group name
            self.channel_name  # Channel name
        )

    async def fetch_prices(self, event):
        # Retrieve trailing prices data from the event
        prices = event['prices']

        # Send the trailing prices to the WebSocket
        await self.send(text_data=json.dumps({
            'prices': prices
        }))
