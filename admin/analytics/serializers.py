from rest_framework import serializers
from quizzes.models import MultipleChoice, Questions, Answer



class ChoiceSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = MultipleChoice 
        fields = ['id', 'choiceText', 'image', 'is_correct', 'count', 'percentage']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_count(self, obj):
        question = obj.question
        audience_list = self.context['audience_list']
        return question.answers.filter(selected_choice=obj, audience__id__in=audience_list).count()


    def get_percentage(self, obj):
        question = obj.question
        audience_list = self.context['audience_list']
        total_count = question.answers.filter(audience__id__in=audience_list).count()
        count = self.get_count(obj)
        return f"{(count / total_count * 100):.2f}" if total_count > 0 else "0.00"

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Questions
        fields = ['id', 'question_text', 'image', 'total_count', 'options']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_total_count(self, obj):
        audience_list = self.context['audience_list']
        total_count = obj.answers.filter(audience__id__in=audience_list).count()  # Count of answers related to this question
        return total_count

    def get_options(self, obj):
        audience_list = self.context['audience_list']
        return ChoiceSerializer(obj.choices.all(), many=True, context={'audience_list': audience_list, 'question': obj}).data  # Passing 'question'
