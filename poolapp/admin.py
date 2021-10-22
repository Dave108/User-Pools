from django.contrib import admin
from .models import Pool, PoolData


# Register your models here.

@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'description', 'is_completed', 'pool1_name', 'pool1_count', 'pool1_percent',
                    'pool2_name', 'pool2_count',
                    'pool2_percent', 'pool3_name', 'pool3_count', 'pool3_percent', 'pool4_name', 'pool4_count',
                    'pool4_percent', 'pool_over_time']


@admin.register(PoolData)
class PoolDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'pool_id']
