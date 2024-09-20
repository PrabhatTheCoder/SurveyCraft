from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizzes/', include('quizzes.urls')),
    path('', lambda request: redirect('quizzes:dashboard')),  # Redirect root URL to dashboard
    path('api/v1/',include('quizzes.urls'))
]
