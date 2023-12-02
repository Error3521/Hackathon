from django.db import models

class Question(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    question = models.TextField()
    answers = models.JSONField()
    result = models.CharField(max_length=10, blank=True, null=True)