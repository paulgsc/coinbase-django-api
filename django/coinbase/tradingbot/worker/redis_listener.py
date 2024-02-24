import redis
import json
import time
from config import REDIS_URL, REDIS_PORT
from .consumer_messenger import ChannelsUpdater
from tradingbot.utlis.utlis import get_selected_coin_prices

CELERY_CHANNELS = 'prices_group'

def get_redis_connection():
    redis_instance = None

    try:
        redis_instance =  redis.Redis(host='localhost', port=6379, db=0)
        redis_instance.ping()
        return redis_instance
    except Exception as e:
        time.sleep(5)
        redis_instance = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=0)
        redis_instance.ping()

    return redis_instance


def publish_message_to_broker(message, channel_name):
    # Publish message to Redis channel
    redis_client = get_redis_connection()
    redis_client.publish(channel_name, json.dumps(message))

def extract_msg(item, type):
    ''' Converting redis message into message send to web socket channel '''
    if item.get('type') is None or item.get('type') != 'pmessage':
        return None
    
    try:
        item_data = json.loads(item['data'].decode('utf8').replace("'", '"'))
    except json.decoder.JSONDecodeError as e:
        # This can happen when task failed
        print(f'this failed: {str(e)}')
        return None
    
    try:
        if item_data['type'] == type:
            data = item_data['prices']
        data = get_selected_coin_prices()
        msg = {"type": type, "prices": data}
    except Exception as e:
        print(f'this failed: {str(e)}')
        return None
    return msg

def main():
    ''' Running redis listener and sending updates to websocket channel '''
    print('start')

    redis_instance = get_redis_connection()
    if redis_instance is None:
        return
    pubsub = redis_instance.pubsub()
    pubsub.psubscribe(CELERY_CHANNELS)

    type = 'fetch_prices'
    group_name = 'prices_group'
    for item in pubsub.listen():
        msg = extract_msg(item, type=type)
        if msg is None:
            continue
        # send to channel
        ChannelsUpdater.update_ws(group_name=group_name, msg=msg)


if __name__ == '__main__':
    main()