from django.urls import path
from .views import SettingsListView

urlpatterns = [
    path('api/settings', SettingsListView.as_view(), name='api-settings'),
]