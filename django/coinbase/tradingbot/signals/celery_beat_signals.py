# app/models.py

import json
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from datetime import datetime, timedelta
from tradingbot.models import CustomPeriodicTask


@receiver(post_save, sender=CustomPeriodicTask)
def create_or_update_celery_task(sender, instance, created, **kwargs):
    schedule_seconds = instance.schedule.total_seconds()
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=int(schedule_seconds), period=IntervalSchedule.SECONDS,
    )
    # Check if task is for site, and if so the task method name is same as instance.name
    if instance.is_site_task:
        defaults = {
            'task': f'app.tasks.tasks.{instance.name}',
            'interval': schedule,
            'enabled': True,
            # Adjust the expiration time as needed
            # 'expires': datetime.now() + timedelta(seconds=30)
        }

    periodic_task, created = PeriodicTask.objects.update_or_create(
        name=instance.name,
        defaults=defaults
    )


@receiver(pre_delete, sender=CustomPeriodicTask)
def delete_related_celery_task(sender, instance, **kwargs):
    try:
        # Get the Celery Beat task using the task name
        celery_task = PeriodicTask.objects.get(
            name=instance.name)

        # Delete the Celery Beat task
        celery_task.delete()
    except PeriodicTask.DoesNotExist:
        pass  # If the Celery Beat task doesn't exist, do nothing
