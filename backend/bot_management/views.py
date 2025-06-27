from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import action
from .models import Intent, Response
from .serializers import (
    AskRequestSerializer,
    AskResponseSerializer,
    IntentSerializer,
    ResponseSerializer
)
from .nlp_engine import NLPEngine
from django.http import JsonResponse
from .exceptions import NLPModelNotTrainedError
import logging
import joblib
import os

logger = logging.getLogger('bot_management')

nlp_engine = NLPEngine()

class AskBotView(APIView):
    def post(self, request):
        request_serializer = AskRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        
        message = request_serializer.validated_data['message']
        context = request_serializer.validated_data.get('context', {})
        
        try:
            logger.info(f"Procesando mensaje: '{message}'")
        
            try:
                # Predecir intención
                intent_id, confidence = nlp_engine.predict_intent(message)
                intent = Intent.objects.filter(id=intent_id).first()
            except NLPModelNotTrainedError:
                    logger.warning("Modelo no entrenado - usando respuesta por defecto")
                    return DRFResponse({
                        "response": "Estoy aprendiendo todavía, por favor intenta más tarde.",
                        "confidence": 0.0
                    })    
            # Obtener respuesta (implementa esta función según tu lógica)
            response_text = self._get_response(intent, context)
            
            response_data = {
                "intent": intent.name if intent else None,
                "response": response_text,
                "confidence": float(confidence)
            }
            
            logger.info(f"Respuesta generada para mensaje: '{message}'")
            return DRFResponse(response_data)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}", exc_info=True)
            return DRFResponse(
                {"error": "Ocurrió un error procesando tu mensaje"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_response(self, intent, context):
        if intent.name == "recordar_nombre" and context.get("nombre"):
            return f"¡Claro, {context['nombre']}! ¿En qué más puedo ayudarte?"
        if not intent:
            logger.debug("No se encontró intención - usando respuesta por defecto")
            return "No entendí tu mensaje. ¿Podrías reformularlo?"
        
        # Buscar respuesta contextual
        if context:
            for response in intent.responses.all():
                if response.conditions and all(
                    context.get(k) == v 
                    for k, v in response.conditions.items()
                ):
                    logger.debug("Usando respuesta contextual")
                    return response.text
        
        # Respuesta por defecto
        default_response = intent.responses.filter(is_default=True).first()
        if default_response:
            logger.debug("Usando respuesta por defecto")
            return default_response.text
        
        logger.warning(f"No hay respuesta configurada para la intención {intent.name}")
        return "No tengo una respuesta configurada para esto."
    
    
class IntentManagementView(generics.ListCreateAPIView):
    queryset = Intent.objects.all()
    serializer_class = IntentSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        
        # Verificar si ya existe
        if Intent.objects.filter(name=name).exists():
            return DRFResponse(
                {
                    "error": f"El intent '{name}' ya existe",
                    "suggestion": "Usa PATCH/PUT para actualizar o elige otro nombre"
                },
                status=status.HTTP_409_CONFLICT
            )
        
        return super().create(request, *args, **kwargs)   
        
class IntentUpsertView(APIView):
    def post(self, request):
        name = request.data.get('name')
        intent, created = Intent.objects.update_or_create(
            name=name,
            defaults={'training_phrases': request.data.get('training_phrases', [])}
        )
        return DRFResponse(
            IntentSerializer(intent).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )     

class TrainNLPView(APIView):
    def post(self, request):
        try:
            logger.info("Entrenamiento iniciado")
            success = nlp_engine.train()
            logger.info("Entrenamiento completado: %s", success)
            return JsonResponse({
                "status": "success" if success else "warning",
                "message": "Modelo entrenado" if success else "No hay datos suficientes"
            })
        except Exception as e:
            logger.error(f"Error en entrenamiento: {str(e)}", exc_info=True)
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

class ResponseListCreateView(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        intent_id = self.request.query_params.get('intent_id')
        if intent_id:
            queryset = queryset.filter(intent_id=intent_id)
        return queryset
    
class ResponseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class SetDefaultResponseView(APIView):
    def patch(self, request, intent_id):
        response_id = request.data.get('response_id')
        try:
            # Quitar el default actual
            Response.objects.filter(intent_id=intent_id, is_default=True).update(is_default=False)
            # Establecer nuevo default
            response = Response.objects.get(id=response_id, intent_id=intent_id)
            response.is_default = True
            response.save()
            return DRFResponse(ResponseSerializer(response).data)
        except Response.DoesNotExist:
            return DRFResponse(
                {"error": "Respuesta no encontrada o no pertenece al intent"},
                status=status.HTTP_404_NOT_FOUND
            )     
            
class EvaluateModelView(APIView):
    def get(self, request):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report

        intents = Intent.objects.filter(is_active=True)
        texts, labels = [], []
        for intent in intents:
            for phrase in intent.training_phrases:
                texts.append(phrase)
                labels.append(intent.id)

        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2)
        nlp_engine.train()  # Reentrenar con todos los datos
        y_pred = nlp_engine.model.predict(X_test)

        report = classification_report(y_test, y_pred, target_names=list(nlp_engine.label_map.values()))
        return Response({"report": report})