from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from security.decorators import permission_required
from django.http import JsonResponse
from .services.erp_client import create_ticket
from .models import ExternalMessageLog
from rest_framework import generics
from .serializers import ExternalMessageLogSerializer
import os


class WhatsAppWebhookView(APIView):
    permission_classes = [IsAuthenticated]
    
    @permission_required('whatsapp.receive_messages')
    def post(self, request):
        message = request.data.get('message')
        sender = request.data.get('sender', 'desconocido')

        if not message:
            return Response({"error": "Mensaje no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        # Registrar mensaje entrante
        ExternalMessageLog.objects.create(
            source="WhatsApp",
            sender=sender,
            message=message,
            direction="in"
        )
        
        # Aquí integrarías con el servicio del bot
        response_text = f"Recibido: {message}"
        
        # Registrar respuesta saliente
        ExternalMessageLog.objects.create(
            source="WhatsApp",
            sender="bot",
            message=response_text,
            direction="out"
        )
        
        return Response({"response": response_text}, status=status.HTTP_200_OK)
    
    def get_qr(request):
        try:
            with open('bot/qr.txt', 'r') as f:
                qr_data = f.read()
            return JsonResponse({'qr': qr_data})
        except FileNotFoundError:
            return JsonResponse({'error': 'QR no generado'}, status=404)
        

class ERPCreateTicketView(APIView):
    def post(self, request):
        subject = request.data.get("subject")
        description = request.data.get("description")
        user_id = request.data.get("user_id")
        
        if not all([subject, description, user_id]):
            return Response({"error": "Faltan campos requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = create_ticket(subject, description, user_id)

            # Registrar mensaje saliente a ERP
            ExternalMessageLog.objects.create(
                source="ERPNext",
                sender=user_id,
                message=f"Ticket creado: {subject}",
                direction="out"
            )

            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class ExternalMessageLogListView(generics.ListAPIView):
    serializer_class = ExternalMessageLogSerializer

    def get_queryset(self):
        queryset = ExternalMessageLog.objects.all().order_by('-timestamp')
        source = self.request.query_params.get('source')
        sender = self.request.query_params.get('sender')
        if source:
            queryset = queryset.filter(source__iexact=source)
        if sender:
            queryset = queryset.filter(sender__icontains=sender)
        return queryset
