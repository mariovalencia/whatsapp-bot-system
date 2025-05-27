from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import action
from .models import Intent, Response
from .serializers import (
    AskRequestSerializer,
    AskResponseSerializer,
    IntentSerializer
)

class AskBotView(APIView):
    """
    Endpoint para interactuar con el bot
    Ejemplo de request:
    {
        "message": "hola",
        "context": {"user_type": "premium"}
    }
    """
    def post(self, request):
        # Validar el request
        request_serializer = AskRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        
        # Procesar mensaje
        intent, confidence = self._find_intent(
            request_serializer.validated_data['message']
        )
        
        # Obtener respuesta
        response_text = self._get_response(
            intent,
            request_serializer.validated_data.get('context', {})
        )
        
        # Construir respuesta
        response_data = {
            "intent": IntentSerializer(intent).data if intent else None,
            "response": response_text,
            "confidence": float(confidence) if confidence else 0.0
        }
        
        response_serializer = AskResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)

    def _find_intent(self, message):
        """
        Lógica simplificada de búsqueda de intención
        Devuelve: (Intent, confidence_score)
        """
        message_lower = message.lower()
        for intent in Intent.objects.all():
            if message_lower in intent.training_phrases:
                return intent, 0.9  # Simulamos un 90% de confianza
        
        return None, None

    def _get_response(self, intent, context):
        if not intent:
            return "Lo siento, no entendí tu mensaje"
        
        # Buscar respuesta con contexto coincidente
        if context:
            for response in intent.responses.all():
                if response.conditions and all(
                    item in context.items() 
                    for item in response.conditions.items()
                ):
                    return response.text
        
        # Buscar respuesta por defecto
        default_response = intent.responses.filter(is_default=True).first()
        return default_response.text if default_response else "No tengo una respuesta configurada"
    
class IntentManagementView(generics.ListCreateAPIView):
    queryset = Intent.objects.all()
    serializer_class = IntentSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        
        # Verificar si ya existe
        if Intent.objects.filter(name=name).exists():
            return Response(
                {
                    "error": f"El intent '{name}' ya existe",
                    "suggestion": "Usa PATCH/PUT para actualizar o elige otro nombre"
                },
                status=status.HTTP_409_CONFLICT
            )
        
        return super().create(request, *args, **kwargs)   
    #@action(detail=False, methods=['POST'])
    #def upsert(self, request):
    #    name = request.data.get('name')
    #    intent, created = Intent.objects.update_or_create(
    #        name=name,
    #        defaults={'training_phrases': request.data.get('training_phrases', [])}
    #    )
    #    return Response(
    #        IntentSerializer(intent).data,
    #       status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    #    )
    
class IntentUpsertView(APIView):
    def post(self, request):
        name = request.data.get('name')
        intent, created = Intent.objects.update_or_create(
            name=name,
            defaults={'training_phrases': request.data.get('training_phrases', [])}
        )
        return Response(
            IntentSerializer(intent).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )     