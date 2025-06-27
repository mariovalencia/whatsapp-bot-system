from rest_framework import serializers
from .models import Intent, Response

# Para el modelo Response
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'intent', 'text', 'is_default', 'conditions', 'priority']
        extra_kwargs = {
            'conditions': {
                'required': False,
                'allow_null': True,
                'help_text': "Condiciones en formato JSON válido"
            }
        }
        
    def validate_conditions(self, value):
        if value is None:
            return value
            
        try:
            # Validar que sea un JSON válido
            if not isinstance(value, dict):
                raise serializers.ValidationError("Las condiciones deben ser un objeto JSON")
            return value
        except (TypeError, ValueError):
            raise serializers.ValidationError("Formato JSON inválido para las condiciones")


# Para el modelo Intent
class IntentSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Intent
        fields = ['id', 'name', 'training_phrases', 'is_active', 'responses', 'metadata']
        extra_kwargs = {
            'name': {
                'validators': []  # Removemos validadores por defecto para manejar manualmente
            },
            'training_phrases': {
                'help_text': "Lista de frases de entrenamiento (ej: ['hola', 'buenos días'])"
            },
            'metadata': {
                'required': False,
                'default': dict
            }
        }
        
    def validate_training_phrases(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Las frases de entrenamiento deben ser una lista")
        if not all(isinstance(phrase, str) for phrase in value):
            raise serializers.ValidationError("Todas las frases de entrenamiento deben ser cadenas de texto")
        return value
        if len(value) != len(set(value)):  # Evitar duplicados
            raise serializers.ValidationError("Hay frases duplicadas.")
        return value

    def validate_name(self, value):
        # Validación personalizada del nombre
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError("El nombre solo puede contener letras, números y guiones bajos")
        return value.lower()  # Normalizamos a minúsculas    


# Para el endpoint de preguntas (AskBotView)
class AskRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=500)
    context = serializers.JSONField(required=False, default=dict)

class AskResponseSerializer(serializers.Serializer):
    intent = IntentSerializer(required=False)
    response = serializers.CharField()
    confidence = serializers.FloatField(default=0.0)