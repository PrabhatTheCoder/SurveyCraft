from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SendPasswordResetEmailSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.tokens import RefreshToken
import json
import uuid
from company.models import App
from .models import CustomUser, AppUsers
from quizzes.serializers import ListAllQuestionSerializer
from quizzes.models import Project, Questions

# Create your views here.



class VerifyAppLoadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        app_id = request.data.get("app_id")
        account_id = request.data.get("account_id")
        device_details = request.data.get("device_details")
        details = json.dumps(device_details)

        if not app_id or not account_id:
            return Response({"error": "Both app_id and account_id are required"},status=status.HTTP_400_BAD_REQUEST,)
                
        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App with the given app_id does not exist"},status=status.HTTP_404_NOT_FOUND,)

        try:
            user = AppUsers.objects.get(id=account_id, app=app)
                
        except AppUsers.DoesNotExist:
            return Response({"error": "User with the given account_id is either not found or not an active owner of the app" },
                status=status.HTTP_404_NOT_FOUND,
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # send_data_to_redis(0, account_id, details, "app_load")

        return Response({"access_token": access_token, "refresh_token": refresh_token},status=status.HTTP_200_OK,)
        


class UpdateAppUserDataView(APIView):                 # Survey and Quiz can be on same page. So we will take project list
    def post(self, request):
        user_id = request.data.get("user_id")
        app_id = request.data.get("app_id")
        attributes = request.data.get("attributes") or []

        if not app_id:
            return Response({"error": "app_id, and project_list are required"},status=status.HTTP_400_BAD_REQUEST,)

        if not user_id:
            uid = str(uuid.uuid4())
            user = AppUsers.objects.create(id=uid, app=App.objects.get(id=app_id), extra_details=attributes)
            user_id = user.id
        try:
            user = AppUsers.objects.get(id=user_id)
        except AppUsers.DoesNotExist:
            user = AppUsers.objects.create(id=user_id, app=App.objects.get(id=app_id), extra_details=attributes)
                
        existing_attributes = user.extra_attributes or []
        
        if isinstance(attributes, list):                 # flattening list of attributes in dictionary for easy updation of data
            for attribute in attributes:                 # attribute would be dict
                if isinstance(attribute, dict):
                    for key, value in attribute.items():
                        existing_attributes[key] = value
                        
        user.extra_details = existing_attributes
        user.save()
        
        return Response(
            {"success": "User Data updated successfully"}, status=status.HTTP_200_OK
        )
            

class UserActionTrackView(APIView):
    def post(self, request):
        project_id = request.data.get("project_id")
        user_id = request.data.get("user_id")
        eventType = request.data.get("event_type")
        eventMessage = "User Action"
        question_id = request.data.get("question_id") or None

        if not project_id or not user_id or not eventType or not eventMessage:
            return Response(
                {"error": "project_id, user_id and eventType are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if eventType == "CLK":
                # send_data_to_redis(project_id, user_id, eventMessage, "click")
                project = Project.objects.get(id=project_id)
                related_model = project.projectType
                if related_model == "QUZ":
                    if question_id:
                        question = Questions.objects.get(id=question_id)
                        question.clicks += 1
                        question.save()
                elif related_model == "SRV":
                    if question_id:
                        question = Questions.objects.get(id=question_id)
                        question.clicks += 1
                        question.save()

            if eventType == "CNV":
                if not question_id:
                    return Response(
                        {"error": "Question ID is required for conversion event"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # send_data_to_redis(project_id, user_id, eventMessage, "click")
                # send_data_to_redis(project_id, user_id, eventMessage, "view")

                question = Questions.objects.get(id=question_id)
                question.clicks += 1
                question.views += 1
                question.save()

            elif eventType == "IMP":
                # send_data_to_redis(project_id, user_id, eventMessage, "impression")
                project = project.objects.get(id=project_id)
                related_model = project.projectType
                if related_model == "QUZ":
                    if question_id:
                        question = Questions.objects.get(id=question_id)
                        question.views += 1
                        question.save()
                elif related_model == "SRV":
                    if question_id:
                        question = Questions.objects.get(id=question_id)
                        question.views += 1
                        question.save()
            return Response({"success": "Event tracked"}, status=status.HTTP_200_OK)
        except project.DoesNotExist:
            return Response(
                {"error": "project not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    
    def put(self, request, *args, **kwargs):
        id = request.user.id
        password = request.data['password']
        try:
            user = CustomUser.objects.get(id=id)
            user.set_password(password) 
            user.save()
            return Response({"message": "Password updated successfully"}, status=200)
        
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    
    
class SendPasswordResetEmailView(APIView):

    def post(self, request, format = None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Password Reset link send. Please Check your Email'}, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@csrf_exempt
def csrf_exempt_password_reset_confirm(request, *args, **kwargs):
    return auth_views.PasswordResetConfirmView.as_view()(request, *args, **kwargs)
