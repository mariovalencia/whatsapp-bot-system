from rest_framework import serializers
from .models import WhatsAppSession, Contact, Conversation, Message

class WhatsAppSessionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo WhatsAppSession
    """
    created_by_username = serializers.SerializerMethodField()
    
    class Meta:
        model = WhatsAppSession
        fields = [
            'id', 'session_id', 'is_active', 'last_qr_code', 
            'qr_generated_at', 'connected_at', 'disconnected_at', 
            'created_by', 'created_by_username', 'created_at'
        ]
        read_only_fields = [
            'id', 'is_active', 'last_qr_code', 'qr_generated_at', 
            'connected_at', 'disconnected_at', 'created_by', 'created_at'
        ]
    
    def get_created_by_username(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return None

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Contact
    """
    class Meta:
        model = Contact
        fields = ['id', 'phone', 'name', 'is_blocked', 'last_interaction', 'created_at']
        read_only_fields = ['id', 'last_interaction', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Conversation
    """
    contact_info = serializers.SerializerMethodField()
    assigned_to_username = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'contact', 'contact_info', 'started_at', 'ended_at', 
            'is_active', 'assigned_to', 'assigned_to_username', 
            'bot_mode', 'message_count', 'last_message'
        ]
        read_only_fields = ['id', 'started_at', 'ended_at']
    
    def get_contact_info(self, obj):
        return {
            'id': obj.contact.id,
            'phone': obj.contact.phone,
            'name': obj.contact.name
        }
    
    def get_assigned_to_username(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.username
        return None
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return {
                'id': last_message.id,
                'content': last_message.content[:100],
                'type': last_message.type,
                'is_from_bot': last_message.is_from_bot,
                'timestamp': last_message.timestamp
            }
        return None

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Message
    """
    sent_by_username = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'message_id', 'content', 'type',
            'sent_by', 'sent_by_username', 'is_from_bot', 'timestamp'
        ]
        read_only_fields = ['id', 'sent_by', 'timestamp']
    
    def get_sent_by_username(self, obj):
        if obj.sent_by:
            return obj.sent_by.username
        return None