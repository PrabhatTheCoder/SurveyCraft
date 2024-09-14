from django.urls import path
from . import views
from .views import quiz_detail

app_name = 'quizzes'

urlpatterns = [
    path('create-quiz/', views.create_quiz, name='create-quiz'),
    path('dashboard/', views.quiz_dashboard, name='dashboard'),
    path('edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('api/quiz/<int:quiz_id>/', quiz_detail, name='quiz-detail'),
    path('api/quizzes/', views.quiz_list_api, name='quiz_list_api'),
]
