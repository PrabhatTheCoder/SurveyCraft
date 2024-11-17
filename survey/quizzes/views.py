from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import QuestionSerializer, MultipleChoiceSerializer, ProjectSerializer, ListQuestionSerializer, QuizSurveyResponseSerializer, DataUploadSerializer, ListAudienceSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import ingest_data_task

class ProjectView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        
        if serializer.is_valid():
            project = serializer.save()
            return Response({'project_id': str(project.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, *args, **kwargs):
        id = request.data["id"]
        instance = Project.objects.get(id=id)
        serializer = ProjectSerializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Updated Sucessfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListProjectView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            apps = user.app.all()  # Ensure the User model has an 'app' field
            
            projects = [project for app in apps for project in app.project_app.all()]
            
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        
        except AttributeError:
            return Response({"error": "User does not have any associated apps"}, status=404)
        
        

        
class QuestionView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            question = serializer.save()
            return Response({'question_id': str(question.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        instance = Questions.objects.get(id=id)
        serializer = QuestionSerializer(instance=instance,data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class MultipleChoiceView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = MultipleChoiceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'multiple_id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        instance = MultipleChoice.objects.get(id=id)
        
        serializer = MultipleChoiceSerializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': "updated succesfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ListQuestionView(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            id = request.GET.get('id')
            if not id:
                return Response({"error": "ID parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

            project = Project.objects.get(id=id)
            queryset = Questions.objects.filter(parent=project)
            if not queryset.exists():
                return Response({"error": "No questions found for this QuizSurveyTask"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ListQuestionSerializer(queryset, many=True) 
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class QuizSurveyResponseView(APIView):
    
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = QuizSurveyResponseSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DataUploadView(APIView):
    def post(self, request):
        serializer = DataUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            audience_id = serializer.validated_data['audience_id']
            app_id = serializer.validated_data['app_id']
            file_path = f'/survey/media/{file.name}'
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            ingest_data_task.delay(file_path,audience_id,app_id)
            return Response({"message": "File upload successful, processing started."}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ListAudienceView(APIView):
    
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, *args, **kwargs):
        user = request.user 
        audiences = Audience.objects.filter(user=user)

        if not audiences.exists():
            return Response({"detail": "No audiences found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListAudienceSerializer(audiences, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AudienceView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        ...