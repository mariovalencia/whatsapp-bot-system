from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class WhatsAppWebhookView(APIView):
    def post(self, request):
        message = request.data.get('message')
        # Aquí integrarías con el servicio del bot
        response_text = f"Recibido: {message}"
        return Response({"response": response_text}, status=status.HTTP_200_OK)