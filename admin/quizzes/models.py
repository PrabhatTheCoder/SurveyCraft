# models.py
from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Allow null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    choices = models.JSONField()  # Or use another field type as needed
    is_required = models.BooleanField(default=False)
    question_type = models.CharField(max_length=20, choices=[('radio', 'Single Answer'), ('checkbox', 'Multiple Answers')])