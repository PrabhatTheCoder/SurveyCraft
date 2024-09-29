from django.contrib import admin
from .models import AllQuiz, Quiz, Multiple

# Inline class for Multiple choices related to a Quiz
class MultipleInline(admin.TabularInline):
    model = Multiple
    extra = 1  # Number of extra forms in the inline section

# Admin class for AllQuiz
@admin.register(AllQuiz)
class AllQuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'expiry_date')
    search_fields = ('name',)
    list_filter = ('expiry_date', 'created_at')

# Admin class for Quiz with inlines for Multiple choices
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'eligible_quiz', 'question_type', 'created_at', 'score')
    search_fields = ('title', 'question_text')
    list_filter = ('question_type', 'created_at', 'eligible_quiz')
    inlines = [MultipleInline]  # Adds the Multiple choices inline to the Quiz admin

# Admin class for Multiple
@admin.register(Multiple)
class MultipleAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'choice_text', 'is_correct')
    search_fields = ('choice_text',)
    list_filter = ('quiz', 'is_correct')
