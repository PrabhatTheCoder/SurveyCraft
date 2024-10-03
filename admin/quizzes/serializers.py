from rest_framework import serializers
# from .models import Quiz, Multiple

# class MultipleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Multiple
#         fields = ['id', 'choice_text','is_correct']
        

# class QuizSerializer(serializers.ModelSerializer):
#     choices = MultipleSerializer(many=True)
#     class Meta:
#         model = Quiz
#         fields = ['id', 'score','title', 'description', 'question_text', 'question_type','choices']
        
#     def create(self, validated_data):
#         choices_data = validated_data.pop('choices')
#         quiz = Quiz.objects.create(**validated_data)
#         for choice_data in choices_data:
#             Multiple.objects.create(quiz=quiz, **choice_data)
#         return quiz
    
#     def update(self, instance, validated_data):
#         choices_data = validated_data.pop('choices', None)
        
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.question_text = validated_data.get('question_text', instance.question_text)
#         instance.question_type = validated_data.get('question_type', instance.question_type)
#         instance.save()
        
#         if choices_data is not None:
#             instance.choices.all().delete() 
#             for choice_data in choices_data:
#                 Multiple.objects.create(quiz=instance, **choice_data)  # Adjust as needed
        
#         return instance


# class ListQuizSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Quiz
#         fields = ['id','title','description']