from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizzes/', include('quizzes.urls')),
    path('api/v1/survey/',include('quizzes.urls')),
    path('api/v1/analytics/', include('analytics.urls'))
]
