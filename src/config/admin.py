from django.contrib import admin
from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'display_name',
        'value',
        'description',
        'group',
        'type',
    )
    search_fields = ('name', 'display_name', 'description', 'group')
    list_filter = ('group', 'type')
