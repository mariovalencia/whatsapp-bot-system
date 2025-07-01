from django.db import models

class Intent(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Nombre de la intención (ej: 'saludo', 'despedida')")
    description = models.TextField(blank=True, null=True)
    training_phrases = models.JSONField(
        default=list,
        help_text="Lista de frases de entrenamiento para el modelo NLP (ej: ['hola', 'buenos días'])"
    )
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)  # Para tags, categorías, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({len(self.training_phrases)} frases)"

class Response(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField(help_text="Texto de respuesta del bot")
    is_default = models.BooleanField(
        default=False,
        help_text="Si es True, se usará cuando no haya coincidencia exacta"
    )
    conditions = models.JSONField(
        blank=True,
        null=True,
        help_text="Condiciones contextuales en formato JSON (opcional)"
    )
    priority = models.IntegerField(default=0)  # Para ordenar respuestas
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-is_default', 'id']

    def __str__(self):
        return f"Respuesta para {self.intent.name} ({'default' if self.is_default else 'personalizada'})"
    

class ConversationLog(models.Model):
    user_phone = models.CharField(max_length=20, help_text="Número de teléfono del usuario")
    message = models.TextField(help_text="Mensaje recibido del usuario")
    intent = models.ForeignKey('Intent', null=True, blank=True, on_delete=models.SET_NULL, help_text="Intención detectada")
    response = models.TextField(help_text="Respuesta generada por el bot")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora del mensaje")

    def __str__(self):
        return f"[{self.timestamp}] {self.user_phone}: {self.message[:30]}..."
    