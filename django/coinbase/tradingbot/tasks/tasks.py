from celery import shared_task
from django.core.management import call_command
import time

@shared_task
def schedule_update_user_access_keys():
     # this will only run once
    print('this is the one and only run!')
    # call_command('update_access_keys')

@shared_task
def print_foo_every_second():
    while True:
        print('foo')
        time.sleep(1)