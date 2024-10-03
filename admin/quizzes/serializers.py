from rest_framework import serializers
from .models import Questions, MultipleChoice

class MultipleChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoice
        fields = ['id', 'choice_text', 'image', 'is_correct']
         
        
        
class QuestionSerializer(serializers.ModelSerializer):
    choices = MultipleChoiceSerializer(many=True)

    class Meta:
        model = Questions
        fields = ['id', 'question_text', 'image', 'project', 'question_type', 'orderMultiple', 'score', 'choices']
        
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        
        question = Questions.objects.create(**validated_data)
        
        for choice_data in choices_data:
            MultipleChoice.objects.create(question=question, **choice_data)
        
        return question
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)
        
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.image = validated_data.get('image', instance.image)
        instance.project = validated_data.get('project', instance.project)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.orderMultiple = validated_data.get('orderMultiple', instance.orderMultiple)
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        
        if choices_data is not None:
            instance.choices.all().delete() 
            for choice_data in choices_data:
                MultipleChoice.objects.create(question=instance, **choice_data)
        
        return instance

class ListSurveySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Questions
        fields = ['id','title','description']