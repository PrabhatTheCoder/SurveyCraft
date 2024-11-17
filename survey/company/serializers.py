from rest_framework import serializers
from .models import App


class AppCreateUpdatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = App
        fields = ['name','URL','app_details']
        
        
class ListAppSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = App
        fields = ['id','name','URL','app_details','isActive','createdAt','updatedAt']
        
class AppDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = App
        fields = ['id','name','URL','app_details','isActive','createdAt','updatedAt']