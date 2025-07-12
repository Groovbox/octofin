from django.urls import path
from .views import SettingsListView, TestJellyfinConnectionView

urlpatterns = [
    path('api/settings', SettingsListView.as_view(), name='api-settings'),
    path('api/settings/jellyfin/test', TestJellyfinConnectionView.as_view(), name='test-jellyfin-connection')
]