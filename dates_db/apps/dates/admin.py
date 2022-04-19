from django.contrib import admin

from dates_db.apps.dates.models import Date


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = [
        'month',
        'day',
        'fact',
    ]
    ordering = ['month']
    list_filter = ('day', 'month')
