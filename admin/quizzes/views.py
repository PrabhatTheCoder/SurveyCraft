from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question
from .forms import QuizForm, QuestionFormSet, ChoiceFormSet
from django.http import JsonResponse
from .serializers import QuizSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


# def create_quiz(request):
#     if request.method == 'POST':
#         form = QuizForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/quizzes/dashboard/')
#     else:
#         form = QuizForm()
#     return render(request, 'quizzes/create_quiz.html', {'quiz_form': form})

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = Quiz.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            return JsonResponse({'message': 'Quiz created successfully!', 'quiz_id': quiz.id}, status=200)
        return JsonResponse({'error': 'Form is invalid'}, status=400)
    
    form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'quiz_form': form})

# View for displaying the quiz dashboard
def quiz_dashboard(request):
    quizzes = Quiz.objects.all()  # Fetch all quizzes
    return render(request, 'quizzes/dashboard.html', {'quizzes': quizzes})

def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_formset = QuestionFormSet(request.POST, instance=quiz)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz_form.save()
            questions = question_formset.save(commit=False)
            for question in questions:
                question.quiz = quiz
                question.save()
                
                choice_formset = ChoiceFormSet(request.POST, instance=question)
                if choice_formset.is_valid():
                    choice_formset.save()
            return redirect('quizzes:quiz_detail', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm(instance=quiz)
        question_formset = QuestionFormSet(instance=quiz)

    return render(request, 'quizzes/edit_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
    })

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


def quiz_detail(request, quiz_id,APIView):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        questions = [
            {
                'id': question.id,
                'title': question.title,
                'question_type': question.question_type,
                'choices': [
                    {'id': choice.id, 'text': choice.text} for choice in question.choices.all()
                ]
            } for question in quiz.questions.all()
        ]

        quiz_data = {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'questions': questions
        }

        return JsonResponse(quiz_data)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

