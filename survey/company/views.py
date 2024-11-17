from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser
from .models import App
from .serializers import  AppCreateUpdatSerializer, ListAppSerializer, AppDetailSerializer
# Create your views here.

## App-Toggle is left

class AppCreateUpdateView(APIView):
    
    def post(self, request,*args, **kwargs):
        
        '''This is used to create app.   'name','URL','app_details' will be input and app_id will be output.
        After saving app, it will automatically assign to the Client'''
        
        serializer = AppCreateUpdatSerializer(data=request.data)
        if serializer.is_valid():
            app_instance = serializer.save()
            user = request.user
            if isinstance(user, CustomUser):
                user.app.add(app_instance)
                user.save()
            return Response({"app_id": app_instance.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request,*args, **kwargs):
        
        '''It is used to update app'''
        
        app_id = request.data['app_id']
        app_instance = App.objects.get(id=app_id)
        serializer = AppCreateUpdatSerializer(app_instance, data=request.data, partial=True)
        if serializer.is_valid():
            app_instance = serializer.save()
            user = request.user
            if isinstance(user, CustomUser):
                user.app.add(app_instance)
                user.save()
            return Response({'status': "App Data Updated Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
 
class ListAppsView(APIView):
    
    '''This is used to fetch all the App data of Client. 
    He will see the list of apps and use app_id to update app data'''
    
    def get(self, request, *args, **kwargs):
        user = request.user
        apps = user.app.all()
        serializer = ListAppSerializer(apps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
class AppDetailView(APIView):
    def get(self, request, *args, **kwargs):
        app_id  = request.GET.get("app_id")
        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return Response({"detail": "App not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppDetailSerializer(app)
        return Response(serializer.data, status=status.HTTP_200_OK)

        