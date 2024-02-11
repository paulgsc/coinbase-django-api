from celery import shared_task
from django.core.management import call_command

@shared_task
def schedule_update_user_access_keys():
    call_command('update_access_keys')