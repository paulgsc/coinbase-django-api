# management/commands/redis_listener.py
from django.core.management.base import BaseCommand
from tradingbot.worker.redis_listener import main

class Command(BaseCommand):
    help = 'Run the Redis listener'

    def handle(self, *args, **options):
        main()
