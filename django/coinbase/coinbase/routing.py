from django.urls import re_path
from tradingbot.consumers.price_data import PricesConsumer

websocket_urlpatterns = [
    re_path(r'ws/coinbase/prices$', PricesConsumer.as_asgi()),

]
