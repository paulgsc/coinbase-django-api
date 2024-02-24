from celery import shared_task
from django.core.management import call_command
from tradingbot.utlis.utlis import get_selected_coin_prices
from tradingbot.worker.redis_listener import publish_message_to_broker 

@shared_task
def fetch_price_data():
    call_command('fetch_price_data')

@shared_task
def pub_message():
    channel_name = 'prices_group'
    # Update cache with the updated deque
    prices_list = get_selected_coin_prices() 
    publish_message_to_broker(
        message={
            'type': 'fetch_prices',
            'prices': prices_list  # Send updated prices to the consumer
        },
        channel_name=channel_name,
    )
