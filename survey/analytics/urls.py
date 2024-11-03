from django.urls import path
from .views import SurveyAnalyticsView

urlpatterns = [
    path('survey-analytics/', SurveyAnalyticsView.as_view()),
]