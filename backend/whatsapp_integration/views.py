from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WhatsAppSession, Contact, Conversation, Message
from .serializers import (
    WhatsAppSessionSerializer, ContactSerializer, 
    ConversationSerializer, MessageSerializer
)
import requests
import os

# URL del servicio de bot (definido en docker-compose)
BOT_SERVICE_URL = os.getenv('BOT_SERVICE_URL', 'http://bot:5000')

class WhatsAppSessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar sesiones de WhatsApp
    """
    queryset = WhatsAppSession.objects.all()
    serializer_class = WhatsAppSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start_session(self, request, pk=None):
        """
        Iniciar una sesión de WhatsApp - genera código QR
        """
        session = self.get_object()
        
        try:
            # Llamar al servicio de bot para iniciar sesión
            response = requests.post(f"{BOT_SERVICE_URL}/start_session", json={
                'session_id': session.session_id
            })
            
            if response.status_code == 200:
                data = response.json()
                # Actualizar información de la sesión
                session.last_qr_code = data.get('qr_code', '')
                session.qr_generated_at = data.get('timestamp')
                session.save()
                
                return Response({
                    'status': 'success',
                    'message': 'Sesión iniciada correctamente',
                    'qr_code': session.last_qr_code
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Error al iniciar sesión'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error al comunicarse con el servicio de bot: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def logout(self, request, pk=None):
        """
        Cerrar una sesión de WhatsApp
        """
        session = self.get_object()
        
        try:
            # Llamar al servicio de bot para cerrar sesión
            response = requests.post(f"{BOT_SERVICE_URL}/logout", json={
                'session_id': session.session_id
            })
            
            if response.status_code == 200:
                # Actualizar información de la sesión
                session.is_active = False
                session.save()
                
                return Response({
                    'status': 'success',
                    'message': 'Sesión cerrada correctamente'
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Error al cerrar sesión'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error al comunicarse con el servicio de bot: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar contactos
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Permitir filtrado por teléfono"""
        queryset = Contact.objects.all()
        phone = self.request.query_params.get('phone', None)
        if phone:
            queryset = queryset.filter(phone=phone)
        return queryset
    
    @action(detail=True, methods=['post'])
    def toggle_block(self, request, pk=None):
        """Bloquear/desbloquear contacto"""
        contact = self.get_object()
        contact.is_blocked = not contact.is_blocked
        contact.save()
        return Response({
            'status': 'success',
            'is_blocked': contact.is_blocked
        })

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar conversaciones
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Permitir filtrado por contacto y estado activo"""
        queryset = Conversation.objects.all()
        contact_id = self.request.query_params.get('contact', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if contact_id:
            queryset = queryset.filter(contact_id=contact_id)
        
        if is_active:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def assign_to_agent(self, request, pk=None):
        """Asignar conversación a un agente"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({
                'status': 'error',
                'message': 'Se requiere ID de usuario'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            
            conversation.assigned_to = user
            conversation.bot_mode = False
            conversation.save()
            
            # Notificar al servicio de bot sobre cambio a modo humano
            try:
                requests.post(f"{BOT_SERVICE_URL}/set_human_mode", json={
                    'phone': conversation.contact.phone,
                    'enable': True
                })
            except Exception as e:
                # Log error pero continuar
                print(f"Error notificando al bot: {str(e)}")
            
            return Response({
                'status': 'success',
                'message': f'Conversación asignada a {user.username}'
            })
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def return_to_bot(self, request, pk=None):
        """Devolver conversación al bot"""
        conversation = self.get_object()
        
        conversation.assigned_to = None
        conversation.bot_mode = True
        conversation.save()
        
        # Notificar al servicio de bot sobre cambio a modo bot
        try:
            requests.post(f"{BOT_SERVICE_URL}/set_human_mode", json={
                'phone': conversation.contact.phone,
                'enable': False
            })
        except Exception as e:
            # Log error pero continuar
            print(f"Error notificando al bot: {str(e)}")
        
        return Response({
            'status': 'success',
            'message': 'Conversación devuelta al bot'
        })
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Enviar mensaje en una conversación"""
        conversation = self.get_object()
        content = request.data.get('content')
        is_from_bot = request.data.get('is_from_bot', False)
        
        if not content:
            return Response({
                'status': 'error',
                'message': 'Se requiere contenido del mensaje'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear mensaje en la base de datos
        message = Message.objects.create(
            conversation=conversation,
            content=content,
            type=request.data.get('type', 'outgoing'),
            sent_by=None if is_from_bot else request.user,
            is_from_bot=is_from_bot
        )
        
        # Si es un mensaje saliente y no es del bot, enviar a través del bot
        if message.type == 'outgoing' and not is_from_bot:
            try:
                requests.post(f"{BOT_SERVICE_URL}/send_message", json={
                    'phone': conversation.contact.phone,
                    'message': content
                })
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': f'Error al enviar mensaje: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(MessageSerializer(message).data)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Obtener mensajes de una conversación"""
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('timestamp')
        page = self.paginate_queryset(messages)
        
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para ver mensajes (solo lectura)
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]