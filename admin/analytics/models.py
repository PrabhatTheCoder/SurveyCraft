from django.db import models
import uuid

class QuizAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)  
    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    time_taken = models.DurationField()
    completion_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} - {self.quiz.title} - Total Score: {self.total_score}"
