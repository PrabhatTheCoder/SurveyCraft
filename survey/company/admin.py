from django.contrib import admin
from .models import App, AppScreen


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'isActive', 'app_details','createdAt', 'updatedAt')


@admin.register(AppScreen)
class AppScreenAdmin(admin.ModelAdmin):
    list_display = ['id','name','App','Image']