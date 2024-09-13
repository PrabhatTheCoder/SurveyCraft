# forms.py
from django import forms
from .models import Quiz
from django.forms import inlineformset_factory
from .models import  Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']  # Include the description field

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'choices', 'is_required', 'question_type']

QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, extra=1, can_delete=True)
