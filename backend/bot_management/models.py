from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Categorías para organizar preguntas y respuestas"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class QuestionAnswer(models.Model):
    """Modelo para almacenar preguntas y respuestas del bot"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField()
    keywords = models.TextField(blank=True, help_text="Keywords separated by commas")
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='created_qa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50]
    
class AlternativeQuestion(models.Model):
    """Preguntas alternativas que apuntan a la misma respuesta"""
    question_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, related_name='alternatives')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]
