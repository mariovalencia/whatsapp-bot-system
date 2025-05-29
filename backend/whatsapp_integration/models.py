from django.db import models

class WhatsAppMessage(models.Model):
    sender = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)