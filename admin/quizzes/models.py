from django.db import models
import uuid

class Quiz(models.Model):
    
    QUESTION_TYPES = (
        ('radio', 'Single Choice'),
        ('checkbox', 'Multiple Choice'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    question_text = models.CharField(max_length=500, default="Default question text")
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.title}: {self.question_text}"
    
class Multiple(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text