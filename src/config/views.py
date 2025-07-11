from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Settings

class SettingsListView(APIView):
    def get(self, request):
        settings_qs = Settings.objects.all()
        settings_dict = {s.name: {'name':s.name, 'value':s.value, 'display_name':s.display_name, 'group': s.group, 'type':s.type} for s in settings_qs}
        return Response(settings_dict)
