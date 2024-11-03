from django.contrib import admin
from django.urls import path, include
from .views import PasswordChange, SendPasswordResetEmailView, csrf_exempt_password_reset_confirm
from django.contrib.auth import views as auth_views
from quizzes.views import QuizSurveyResponseView


urlpatterns = [
    path('change-password/',PasswordChange.as_view()),
    path('reset-password/',SendPasswordResetEmailView.as_view()),
    path('reset-password/<uidb64>/<token>/', csrf_exempt_password_reset_confirm, name='password_reset_confirm'),

    path('user-response/',QuizSurveyResponseView.as_view()),
]