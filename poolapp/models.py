import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone
from datetime import timedelta


# Create your models here.

class Pool(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    pool1_name = models.CharField(null=False, max_length=100)
    pool1_count = models.FloatField(default=0)
    pool1_percent = models.FloatField(default=0)
    pool2_name = models.CharField(null=False, max_length=100)
    pool2_count = models.FloatField(default=0)
    pool2_percent = models.FloatField(default=0)
    pool3_name = models.CharField(null=True, max_length=100, blank=True)
    pool3_count = models.FloatField(default=0)
    pool3_percent = models.FloatField(default=0)
    pool4_name = models.CharField(null=True, max_length=100, blank=True)
    pool4_count = models.FloatField(default=0)
    pool4_percent = models.FloatField(default=0)
    pool_over_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class PoolData(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pool_id = models.ForeignKey(Pool, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username


@receiver(post_save, sender=Pool)
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        data = Pool.objects.filter(name=instance)
        print(sender.pool_over_time, "SENDER")
        print(instance, "instance")
        print(data)
        ltm = datetime.datetime.now() + timedelta(days=1)
        print(ltm.day)
        # celery code to call task and create cron tab time table
        unique_id = get_random_string(length=4)
        # (hour=hour, minute=minutes, day_of_week = '0,1,2,3,4,5,6', day_of_month = 1, month_of_year = 1)
        schedule, created = CrontabSchedule.objects.get_or_create(hour=ltm.hour, minute=ltm.minute)
        task = PeriodicTask.objects.create(crontab=schedule, name="task_scheduled_" + unique_id,
                                           task='poolapp.tasks.time_over')
        print("celery set-------")
