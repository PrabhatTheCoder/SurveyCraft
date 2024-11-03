from rest_framework import serializers
from .models import Questions, MultipleChoice, Project, QuizSurveyTaskResponse
from datetime import timedelta


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name','screen','status','projectType','audience','app','expiry_date']
        
        extra_kwargs = {
            'expiry_date': {'required': False}, 
        }
        
    def create(self, validated_data):
        project = Project(**validated_data)
        
        project.save() 
        
        project.expiry_date = project.createdAt + timedelta(days=4)  # Set expiry date
        project.save()  # Save again to update the expiry_date

        return project
        


class MultipleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoice
        fields = ['id', 'choiceText', 'question','image', 'is_correct','color','height','width']
         
        
        
# class ListQuestionSerializer(serializers.ModelSerializer):
#     choices = MultipleChoiceSerializer(many=True)

#     class Meta:
#         model = Questions
#         fields = ['id', 'question_text', 'image', 'project', 'question_type', 'orderMultiple', 'score', 'choices']
        
    # def create(self, validated_data):
    #     choices_data = validated_data.pop('choices')
        
    #     question = Questions.objects.create(**validated_data)
        
    #     for choice_data in choices_data:
    #         MultipleChoice.objects.create(question=question, **choice_data)
        
    #     return question
    
    # def update(self, instance, validated_data):
    #     choices_data = validated_data.pop('choices', None)
        
    #     instance.question_text = validated_data.get('question_text', instance.question_text)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.survey = validated_data.get('survey', instance.survey)
    #     instance.save()
        
    #     if choices_data is not None:
    #         instance.choices.all().delete() 
    #         for choice_data in choices_data:
    #             MultipleChoice.objects.create(question=instance, **choice_data)
        
    #     return instance
    
class ListQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField() 

    class Meta:
        model = Questions
        fields = ['id', 'question_text', 'question_type','image', 'order', 'color', 'height', 'width', 'choices']

        extra_kwargs = {
            'question_type': {'required': True}, 
        }

    def get_choices(self, obj):
        queryset = MultipleChoice.objects.filter(question=obj) 
        multiples = MultipleChoiceSerializer(queryset, many=True)
        return multiples.data  


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ['question_text', 'image', 'parent', 'order', 'color', 'height', 'width']

  

class QuizSurveyResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizSurveyTaskResponse
        fields = ['user','question','selected_choice']
        
   
   
# AppUser App Segment.. this data will be show on App where user can send the response
   
class ListMultipleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoice
        fields = ['id', 'choiceText', 'question','image', 'color','height','width']
       
   
        
class ListAllQuestionSerializer(serializers.ModelSerializer):   # Question in App
    choices = serializers.SerializerMethodField() 

    class Meta:
        model = Questions
        fields = ['id', 'question_text', 'question_type','image', 'order', 'color', 'height', 'width', 'choices']

        extra_kwargs = {
            'question_type': {'required': True}, 
        }

    def get_choices(self, obj):
        queryset = MultipleChoice.objects.filter(question=obj) 
        multiples = ListMultipleChoiceSerializer(queryset, many=True)
        return multiples.data  
        