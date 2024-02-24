from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ChannelsUpdater:

    @staticmethod
    def update_ws(group_name, msg):
        # send to channel
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group_name, msg)