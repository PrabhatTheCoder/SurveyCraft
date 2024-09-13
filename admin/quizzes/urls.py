from django.urls import path
from . import views
from .views import QuizDetailView

urlpatterns = [
    path('create-quiz/', views.create_quiz, name='create-quiz'),
    path('dashboard/', views.quiz_dashboard, name='quiz-dashboard'),
    path('quizzes/edit/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('api/quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('api/quizzes/', views.quiz_list_api, name='quiz_list_api'),
]
