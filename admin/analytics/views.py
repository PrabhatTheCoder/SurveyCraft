from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizzes.models import Project
from .serializers import QuestionSerializer
from django.shortcuts import get_object_or_404



class SurveyAnalyticsView(APIView):

    def post(self, request, *args, **kwargs):

        project_id = request.data['id']
        audience_list = request.data['audience']

        if not project_id:
            return Response({"error": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = get_object_or_404(Project, id=project_id) 

            if project.projectType == 'SRV':
                questions = project.questions.prefetch_related('choices').all()

                question_data = QuestionSerializer(questions, many=True, context={'audience_list': audience_list}).data

                return Response({"questions": question_data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid project type"}, status=status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
