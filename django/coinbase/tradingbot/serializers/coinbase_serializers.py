from rest_framework import serializers
from tradingbot.models import Coin

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        exclude = ['id']
        read_only_fields = ['created_at']  


