from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from security.decorators import permission_required
from django.http import JsonResponse
import os

class WhatsAppWebhookView(APIView):
    permission_classes = [IsAuthenticated]
    
    @permission_required('whatsapp.receive_messages')
    def post(self, request):
        message = request.data.get('message')
        # Aquí integrarías con el servicio del bot
        response_text = f"Recibido: {message}"
        return Response({"response": response_text}, status=status.HTTP_200_OK)
    
    def get_qr(request):
        try:
            with open('bot/qr.txt', 'r') as f:
                qr_data = f.read()
            return JsonResponse({'qr': qr_data})
        except FileNotFoundError:
            return JsonResponse({'error': 'QR no generado'}, status=404)