from django.urls import path
from .views import ListAppsView, AppCreateUpdateView, AppDetailView

app_name = 'company'

urlpatterns = [
    path('create-app/',AppCreateUpdateView.as_view()),
    path('update-app/',AppCreateUpdateView.as_view()),
    
    path('list-apps/',ListAppsView.as_view()),
    path('app/',AppDetailView.as_view())             ## Query-Params
    
]
