from django import forms
from .models import Quiz, Question, Choice
from django.forms import inlineformset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']

# Formset for dynamically adding/editing questions
QuestionFormSet = inlineformset_factory(Quiz, Question, fields=('question_text', 'question_type'), extra=1, can_delete=True)

# Formset for dynamically adding/editing choices
ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text', 'is_correct'), extra=1, can_delete=True)
