from django.contrib import admin
from .models import Quiz, Multiple

# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'question_type','created_at', 'updated_at')
    search_fields = ('title', 'question_text')
    list_filter = ('question_type', 'created_at')
    fields = ('title', 'description', 'question_text', 'question_type')
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(Multiple)
class MultipleAdmin(admin.ModelAdmin):
    list_display = ['id','choice_text', 'is_correct']

