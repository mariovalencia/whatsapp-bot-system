from django.db import models
from django.contrib.auth.models import User

class WhatsAppSession(models.Model):
    """Modelo para gestionar sesiones de whatsapp"""
    session_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    last_qr_code = models.TextField(blank=True)
    qr_generated_at = models.DateTimeField(null=True, blank=True)
    connected_at = models.DateTimeField(null=True, blank=True)
    disconnected_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} - {'Active' if self.is_active else 'Inactive'}"
    
class Contact(models.Model):
    """Contactos de Whatsapp"""
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_blocked = models.BooleanField(default=False)
    last_interaction = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
    
class Conversation(models.Model):
    """Conversaciones con contactos"""
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bot_mode = models.BooleanField(default=True)

    def __str__(self):
        return f"Conversation with {self.contact.name} - {'Active' if self.is_active else 'Ended'}"
    
class Message(models.Model):
    """Mensajes individuales en una conversacion"""
    TYPE_CHOICES = [
        ('incoming','Incoming'),
        ('outgoing','Outgoing'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_id = models.CharField(max_length=100, blank=True) # ID del mensaje en WhatsApp
    content = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_from_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} message in {self.conversation}"