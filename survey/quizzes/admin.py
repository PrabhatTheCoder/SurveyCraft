from django.contrib import admin
from .models import Audience, Project, Questions, MultipleChoice, QuizSurveyTaskResponse

@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'createdAt', 'updatedAt')
    search_fields = ('name', 'description')
    list_filter = ('createdAt', 'updatedAt')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'projectType', 'audience', 'createdAt', 'expiry_date')
    search_fields = ('name', 'audience__name')
    list_filter = ('status', 'projectType', 'audience', 'createdAt')

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'parent', 'question_type', 'created_at', 'score','color','height','width')
    search_fields = ('question_text', 'parent__name')
    list_filter = ('question_type', 'parent', 'created_at')

@admin.register(MultipleChoice)
class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choiceText', 'is_correct', 'count','color','height','width')
    search_fields = ('choiceText', 'question__question_text')
    list_filter = ('is_correct', 'question')

@admin.register(QuizSurveyTaskResponse)
class QuizSurveyTaskResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'selected_choice')
    search_fields = ('user__name', 'question__question_text')
    list_filter = ('question', 'user')