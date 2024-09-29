from django.contrib import admin
from .models import QuizAnalytics

# Register your models here.
class QuizAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'total_score', 'correct_answers', 'total_questions', 'time_taken', 'completion_date')
    list_filter = ('quiz', 'completion_date')
    search_fields = ('user__first_name', 'user__email', 'quiz__title')

# Registering the model
admin.site.register(QuizAnalytics, QuizAnalyticsAdmin)