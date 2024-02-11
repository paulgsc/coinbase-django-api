from django.core.management.base import BaseCommand
from tradingbot.models import Coin

class Command(BaseCommand):
    help = 'Populate the Coin model with 5 records'

    def handle(self, *args, **options):
        coins_data = [
            {'symbol': 'BTC', 'full_name': 'Bitcoin', 'description': 'Description of Bitcoin'},
            {'symbol': 'ETH', 'full_name': 'Ethereum', 'description': 'Description of Ethereum'},
            {'symbol': 'ADA', 'full_name': 'Cardano', 'description': 'Description of Cardano'},
            {'symbol': 'XRP', 'full_name': 'Ripple', 'description': 'Description of Ripple'},
            {'symbol': 'LTC', 'full_name': 'Litecoin', 'description': 'Description of Litecoin'},
        ]

        for data in coins_data:
            coin, created = Coin.objects.get_or_create(
                symbol=data['symbol'],
                defaults={'full_name': data['full_name'], 'description': data['description']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created coin: {coin}'))
            else:
                self.stdout.write(self.style.WARNING(f'Coin {coin} already exists'))

