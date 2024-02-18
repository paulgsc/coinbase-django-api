from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache 

class PricesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.selected_coin = None  # Initialize selected coin

        # Accept the WebSocket connection
        await self.accept()

        # Add the consumer to the 'prices_group' group
        await self.channel_layer.group_add(
            'prices_group',  # Group name
            self.channel_name  # Channel name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'select_coin':
            self.selected_coin = data.get('coin_symbol')
            cache.set('selected_coin_symbol', self.selected_coin)
        
        # Retrieve prices from the cache based on the selected coin symbol
        prices_key = f'{self.selected_coin}_prices'
        selected_prices = cache.get(prices_key, [])

        # Send the selected prices to the WebSocket
        await self.send(text_data=json.dumps({
            'prices': selected_prices
        }))

    async def disconnect(self, close_code):
        # Remove the consumer from the 'prices_group' group
        await self.channel_layer.group_discard(
            'prices_group',  # Group name
            self.channel_name  # Channel name
        )

    async def fetch_prices(self, event):
        # Handle prices update and message client
        if event and 'prices' in event:
            # Retrieve trailing prices data from the event
            prices = event['prices']

            # Send the trailing prices to the WebSocket
            await self.send(text_data=json.dumps({
                'prices': prices
            }))
  
    
