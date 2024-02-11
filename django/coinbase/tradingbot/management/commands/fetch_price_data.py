import json
from django.core.management.base import BaseCommand
import requests
from django.core.cache import cache
import time
from collections import deque
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Fetches prices from Coinbase API and updates Redis cache with trailing dataset'

    def handle(self, *args, **kwargs):
        # Define your array of coins
        coins = ['AAVE-USD', 'BTC-USD', 'ETH-USD']
        type = 'spot'

        for coin in coins:
            url = f'https://api.coinbase.com/v2/prices/{coin}/{type}'
            response = requests.get(url)

            if response.status_code == 200:
                price_data = response.json()

                # Get existing prices from cache or initialize an empty deque
                prices_key = f'{coin}_prices'
                existing_prices = cache.get(prices_key)
                prices = deque(existing_prices, maxlen=1000) if existing_prices else deque(maxlen=1000)

                # Append new price data to the deque
                prices.append(price_data)

                # Update cache with the updated deque
                cache.set(prices_key, list(prices), timeout=3600 * 3)  # Set expiry to 3 hours

                # Publish prices update to the WebSocket consumer
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'prices_group',  # Group name where the consumer is listening
                    {
                        'type': 'fetch_prices',
                        'prices': list(prices)  # Send updated prices to the consumer
                    }
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully updated {coin} prices in cache'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch {coin} prices'))

