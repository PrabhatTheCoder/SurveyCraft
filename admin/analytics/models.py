from django.db import models
    
    
class QuizAnalytics(models.Model):
    user = models.ForeignKey("users.CustomeUser", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey("quizzes.Quiz")  
    total_score = models.IntegerField(default=0)
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    time_taken = models.DurationField()
    completion_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} - {self.quiz.title} - Total Score: {self.total_score}"