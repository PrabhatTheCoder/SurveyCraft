from rest_framework import serializers
from .models import QuizAnalytics

class ContestantEvalutionSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = QuizAnalytics
        fields = ['user','total_score','correct_answers','total_questions','time_taken']
        
        