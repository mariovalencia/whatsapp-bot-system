from django.db import models

class ExternalMessageLog(models.Model):
    source = models.CharField(max_length=50, help_text="Origen del mensaje: WhatsApp, ERPNext, etc.")
    sender = models.CharField(max_length=50)
    message = models.TextField()
    direction = models.CharField(max_length=10, choices=[('in', 'Entrante'), ('out', 'Saliente')])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"[{self.timestamp}] {self.source} - {self.sender}: {self.message[:30]}..."