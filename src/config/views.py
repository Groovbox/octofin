from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Settings
from .serializers import SettingsSerializer

import requests

class SettingsListView(APIView):
    def get(self, request):
        settings = Settings.objects.all()
        serializer = SettingsSerializer(settings, many=True)
        return Response({s['name']: s for s in serializer.data})

    def post(self, request):
        name = request.data.get('name')
        value = request.data.get('value')

        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            setting = Settings.objects.get(name=name)
            setting.value = value
            setting.save()
            serializer = SettingsSerializer(setting)
            return Response(serializer.data)
        except Settings.DoesNotExist:
            return Response({'error': f'Setting with name "{name}" not found'}, status=status.HTTP_404_NOT_FOUND)


class TestJellyfinConnectionView(APIView):
    def post(self, request):
        # Try to fetch API key and server URL from database
        try:
            api_key = Settings.objects.get(name='jellyfin_api_key').value
            jellyfin_url = Settings.objects.get(name='jellyfin_server_url').value
        except Settings.DoesNotExist:
            return Response({'success': False, 'error': 'Missing Jellyfin API key or server URL in settings'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Normalize server URL (ensure it ends with a slash)
        if not jellyfin_url.endswith('/'):
            jellyfin_url += '/'

        # Construct full API endpoint to test
        test_url = jellyfin_url + 'System/Info'

        # Construct correct Authorization header
        headers = {
            'Authorization': f'MediaBrowser Token="{api_key}"'
        }

        try:
            response = requests.get(test_url, headers=headers, timeout=5)

            if response.status_code == 200:
                return Response({'success': True})
            else:
                return Response({
                    'success': False,
                    'status_code': response.status_code,
                    'response': response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                }, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)