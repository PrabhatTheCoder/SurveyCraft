from django.urls import path
from .views import ProjectView, ListProjectView, QuestionView, MultipleChoiceView, ListQuestionView, QuizSurveyResponseView, DataUploadView, ListAudienceView

app_name = 'quizzes'

urlpatterns = [
#     path('create-quiz/',NewQuiz.as_view()),
#     path('update-quiz/',UpdateQuiz.as_view()),
#     path('list-quizes/',ListQuizView.as_view())

    path('create-project/',ProjectView.as_view()),
    path('update-project/',ProjectView.as_view()),
    path('list-project/',ListProjectView.as_view()),
    
    path('create-question/',QuestionView.as_view()),
    path('update-question/<uuid:id>/',QuestionView.as_view()),
    path('list-questions/',ListQuestionView.as_view()),
    
    path('create-multiple/',MultipleChoiceView.as_view()),
    path('update-multiple/<uuid:id>/',MultipleChoiceView.as_view()),
    
    path('upload-file/', DataUploadView.as_view()),
    path('list-audience/', ListAudienceView.as_view())
    
    
]
