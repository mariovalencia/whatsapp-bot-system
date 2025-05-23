from django.db import models

class Question(models.Model):
    text = models.TextField()
    intent = models.CharField(max_length=100)
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()