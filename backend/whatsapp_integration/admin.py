from django.contrib import admin

from django.contrib import admin
from .models import WhatsAppSession, Contact, Conversation, Message

@admin.register(WhatsAppSession)
class WhatsAppSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'session_id', 'is_active', 'connected_at', 'disconnected_at')
    search_fields = ('name', 'session_id')
    list_filter = ('is_active',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'last_interaction')
    search_fields = ('phone', 'name')
    list_filter = ('last_interaction',)

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at', 'type', 'content', 'is_from_bot', 'is_read')
    can_delete = False
    max_num = 0

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('contact', 'is_active', 'bot_mode', 'assigned_to', 'created_at')
    list_filter = ('is_active', 'bot_mode')
    search_fields = ('contact__phone', 'contact__name')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'type', 'content_preview', 'is_from_bot', 'is_read', 'created_at')
    list_filter = ('type', 'is_from_bot', 'is_read')
    search_fields = ('content', 'conversation__contact__name', 'conversation__contact__phone')
    
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Contenido'
