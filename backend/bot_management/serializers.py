from rest_framework import serializers
from .models import Intent, Response

# Para el modelo Intent
class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = ['id', 'name', 'training_phrases']

# Para el modelo Response
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'intent', 'text', 'is_default']

# Para el endpoint de preguntas (AskBotView)
class AskRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=500)
    context = serializers.JSONField(required=False, default=dict)

class AskResponseSerializer(serializers.Serializer):
    intent = IntentSerializer(required=False)
    response = serializers.CharField()
    confidence = serializers.FloatField(default=0.0)