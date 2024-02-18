import json
from django.core.management.base import BaseCommand
import requests
from django.core.cache import cache
import time
from collections import deque
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from tradingbot.models import Coin

class Command(BaseCommand):
    help = 'Fetches prices from Coinbase API and updates Redis cache with trailing dataset'

    def handle(self, *args, **kwargs):
        # Fetch up to five coins from the model
        coins = Coin.objects.all()[:5]

        if not coins:
            self.stdout.write(self.style.WARNING('No coins found in the database. Exiting command.'))
            return

        for coin in coins:
            # Fetch price data from the first endpoint
            price_url = f'https://api.coinbase.com/v2/prices/{coin.symbol}-USD/spot'
            price_response = requests.get(price_url)

            if price_response.status_code == 200:
                price_data = price_response.json()['data']
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch {coin} prices'))
                continue

            # Fetch timestamp data from the second endpoint
            time_response = requests.get('https://api.coinbase.com/v2/time')
            if time_response.status_code == 200:
                timestamp = time_response.json()['data']['epoch']
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch timestamp'))
                continue

            # Combine price data and timestamp
            combined_data = {**price_data, 'timestamp': timestamp}

            # Get existing prices from cache or initialize an empty deque
            prices_key = f'{coin.symbol}_prices'
            existing_prices = cache.get(prices_key)
            prices = deque(existing_prices, maxlen=1000) if existing_prices else deque(maxlen=1000)

            # Append new price data to the deque
            prices.append(combined_data)

            # Convert the prices to list
            prices_list = list(prices)

            # Update cache with the updated deque
            cache.set(prices_key, prices_list, timeout=3600 * 3)  # Set expiry to 3 hours

            # Retrieve the selected coin symbol from the cache that client is viewing
            selected_coin_symbol = cache.get('selected_coin_symbol', 'BTC')  # Default to BTC if not set
            
            # Publish prices update to the WebSocket consumer
            if selected_coin_symbol == coin.symbol:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'prices_group',  # Group name where the consumer is listening
                    {
                        'type': 'fetch_prices',
                        'prices': prices_list  # Send updated prices to the consumer
                    }
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully updated {coin} prices in cache'))

