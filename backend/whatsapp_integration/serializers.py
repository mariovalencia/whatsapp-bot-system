from rest_framework import serializers
from .models import ExternalMessageLog

class ExternalMessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalMessageLog
        fields = ['id', 'source', 'sender', 'message', 'direction', 'timestamp']
