from django.urls import path
from .views import NewQuiz, UpdateQuiz

app_name = 'quizzes'

urlpatterns = [
    path('create-quiz/',NewQuiz.as_view()),
    path('update-quiz/',UpdateQuiz.as_view()),
    
]
