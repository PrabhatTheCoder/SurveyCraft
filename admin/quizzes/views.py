from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question
from .forms import QuizForm, QuestionFormSet, QuestionForm
from django.http import JsonResponse
from .serializers import QuizSerializer
from rest_framework import generics

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/quizzes/dashboard/')
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'quiz_form': form})

# View for displaying the quiz dashboard
def quiz_dashboard(request):
    quizzes = Quiz.objects.all()  # Fetch all quizzes from the database
    return render(request, 'quizzes/dashboard.html', {'quizzes': quizzes})

def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        formset = QuestionFormSet(request.POST, instance=quiz)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('/quizzes/dashboard/')
    else:
        form = QuizForm(instance=quiz)
        formset = QuestionFormSet(instance=quiz)
    
    return render(request, 'quizzes/edit_quiz.html', {'quiz_form': form, 'formset': formset, 'quiz': quiz})

def quiz_list_api(request):
    quizzes = Quiz.objects.all()
    data = []
    for quiz in quizzes:
        data.append({
            'id': quiz.id,
            'title': quiz.title,
            'created_at': quiz.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'quizzes': data})

