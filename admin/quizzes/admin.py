from django.contrib import admin
from .models import Audience, Project, Questions, MultipleChoice, Answer

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
    list_display = ('id', 'question_text', 'project', 'question_type', 'created_at', 'score')
    search_fields = ('question_text', 'project__name')
    list_filter = ('question_type', 'project', 'created_at')

@admin.register(MultipleChoice)
class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choiceText', 'is_correct', 'count')
    search_fields = ('choiceText', 'question__question_text')
    list_filter = ('is_correct', 'question')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'selected_choice', 'response')
    search_fields = ('user__username', 'question__question_text')
    list_filter = ('question', 'user')
