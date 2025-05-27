from django.contrib import admin
from .models import Intent, Response

@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ('name', 'training_phrases_count', 'created_at')
    search_fields = ('name',)

    def training_phrases_count(self, obj):
        return len(obj.training_phrases)
    training_phrases_count.short_description = "Frases"

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('intent', 'text_preview', 'is_default')
    list_filter = ('is_default', 'intent')
    raw_id_fields = ('intent',)

    def text_preview(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Respuesta"