from django.shortcuts import render
from rest_framework.views import APIView
from quizzes.models import Multiple
from .models import QuizAnalytics
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class ContestantEvaluation(APIView):
    
    def calculate_score(user_answers):
        total_score = 0
        correct_answers = 0

        multiple_objects = Multiple.objects.filter(id__in=user_answers)
        for obj in multiple_objects:
            if obj.is_correct == True:
                score = obj.quiz.score
                total_score += score
                correct_answers += 1
        return total_score, correct_answers
    
    
    def post(self, request, *args, **kwargs):
        user = request.user
        user_answers = request.data['user_answers']
        total_score, correct_answers = self.calculate_score(user_answers)
        
        multiple_object = Multiple.objects.filter(id=user_answers[0]).first()
        if not multiple_object:
            return Response({"error": "Invalid answers provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        quiz = multiple_object.quiz
        total_questions = quiz.choices.count()

        QuizAnalytics.objects.create(
            user=user,
            quiz=quiz,
            total_score=total_score,
            correct_answers=correct_answers,
            total_questions=total_questions,
            time_taken=timezone.now() - request.data.get('start_time', timezone.now())
        )
        return Response({"total_score": total_score,"correct_answers": correct_answers}, status=status.HTTP_200_OK)