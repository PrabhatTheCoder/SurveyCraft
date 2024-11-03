from rest_framework import serializers
from .utils import Util
from .models import CustomUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        model = CustomUser
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email = email).exists():
            user = CustomUser.objects.get(email = email)
            
            uid = urlsafe_base64_encode(force_bytes(user.id))
            
            token = PasswordResetTokenGenerator().make_token(user) 
            
            link = 'http://127.0.0.1:8000/api/v1/users/reset-password/' + uid + '/' + token + '/'
            print(link)
            
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject' : 'Reset Your Password',
                'body': body,
                'to_email' : user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValueError("You are not a selected User")
        
        
