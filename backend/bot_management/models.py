from django.db import models

class Intent(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Nombre de la intención (ej: 'saludo', 'despedida')")
    training_phrases = models.JSONField(
        default=list,
        help_text="Lista de frases de entrenamiento para el modelo NLP (ej: ['hola', 'buenos días'])"
    )
    created_at = models.DateTimeField(auto_now_add=True)

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

    class Meta:
        ordering = ['-is_default', 'id']

    def __str__(self):
        return f"Respuesta para {self.intent.name} ({'default' if self.is_default else 'personalizada'})"