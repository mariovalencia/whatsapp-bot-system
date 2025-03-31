from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.utils import timezone

from security.models import Role, Permission, UserProfile
from bot_management.models import Category, QuestionAnswer, AlternativeQuestion
from whatsapp_integration.models import WhatsAppSession, Contact, Conversation, Message
from .serializers import (
    UserSerializer, RoleSerializer, PermissionSerializer,
    CategorySerializer, QuestionAnswerSerializer, QuestionAnswerDetailSerializer,
    WhatsAppSessionSerializer, ContactSerializer, ConversationSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar usuarios"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar roles"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar permisos"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar categorías de preguntas/respuestas"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionAnswerViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar preguntas y respuestas"""
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Cambia el serializador según la acción"""
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return QuestionAnswerDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Asigna el usuario actual como creador"""
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Filtra preguntas/respuestas por categoría"""
        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = self.queryset.filter(category_id=category_id)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "Category ID required"}, status=status.HTTP_400_BAD_REQUEST)

class WhatsAppSessionViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar sesiones de WhatsApp"""
    queryset = WhatsAppSession.objects.all()
    serializer_class = WhatsAppSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Asigna el usuario actual como creador de la sesión"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def generate_qr(self, request, pk=None):
        """Solicita generación de código QR para esta sesión"""
        session = self.get_object()
        # Actualizamos el timestamp y marcamos como pendiente
        # El código QR real será generado por el servicio bot
        session.qr_generated_at = timezone.now()
        session.is_active = False
        session.save()
        return Response({"message": "QR code generation requested"})

    @action(detail=True, methods=['post'])
    def disconnect(self, request, pk=None):
        """Desconecta una sesión activa"""
        session = self.get_object()
        if session.is_active:
            session.is_active = False
            session.disconnected_at = timezone.now()
            session.save()
            return Response({"message": "WhatsApp session disconnected"})
        return Response({"error": "Session is not active"}, status=status.HTTP_400_BAD_REQUEST)

class ContactViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar contactos de WhatsApp"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Bloquea un contacto"""
        contact = self.get_object()
        contact.is_blocked = True
        contact.save()
        return Response({"message": "Contact blocked"})
    
    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        """Desbloquea un contacto"""
        contact = self.get_object()
        contact.is_blocked = False
        contact.save()
        return Response({"message": "Contact unblocked"})

class ConversationViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar conversaciones"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Asigna una conversación al usuario autenticado"""
        conversation = self.get_object()
        conversation.assigned_to = request.user
        conversation.bot_mode = False
        conversation.save()
        return Response({"message": "Conversation assigned"})
    
    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        """Libera la conversación para que vuelva al bot"""
        conversation = self.get_object()
        conversation.assigned_to = None
        conversation.bot_mode = True
        conversation.save()
        return Response({"message": "Conversation released to bot"})
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """Finaliza una conversación"""
        conversation = self.get_object()
        conversation.is_active = False
        conversation.ended_at = timezone.now()
        conversation.assigned_to = None
        conversation.save()
        return Response({"message": "Conversation ended"})
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Obtiene los mensajes de una conversación"""
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('timestamp')
        from .serializers import MessageSerializer
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Envía un mensaje en una conversación"""
        conversation = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Creamos el mensaje en la base de datos
        message = Message.objects.create(
            conversation=conversation,
            content=content,
            type='outgoing',
            sent_by=request.user,
            is_from_bot=False
        )
        
        # Aquí se enviaría el mensaje a través del servicio de bot
        # (Implementación pendiente en el servicio de bot)
        
        from .serializers import MessageSerializer
        return Response(MessageSerializer(message).data)