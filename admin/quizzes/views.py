from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from .serializers import QuizSerializer, ListQuizSerializer


# class NewQuiz(APIView):
    
#     def post(self, request, *args, **kwargs):
#         serializer = QuizSerializer(data=request.data)
        
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class UpdateQuiz(APIView):
    
#     def post(self, request, *args, **kwargs):
#         id = request.data['id']
#         instance = Quiz.objects.get(id=id)
#         serializer = QuizSerializer(instance=instance,data=request.data, partial=True)
        
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class ListQuizView(APIView):
#     def get(self, request, *args, **kwargs):
#         queryset = Quiz.objects.all()
#         serializer = ListQuizSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        