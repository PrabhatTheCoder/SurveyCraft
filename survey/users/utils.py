import os
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import environ
env = environ.Env()
environ.Env.read_env()

class Util:
    
    @staticmethod
    def send_email(data):
        subject = data["subject"]
        body = data['body']
        from_email = env("EMAIL_USER") 
        to_email = data.get("to_email")  

        if not from_email:
            raise ValueError("EMAIL_USER environment variable is not set")

        if not to_email:
            raise ValueError("to_email is missing from data")

        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=from_email,
                to=[to_email],
            )
            email.send()  

        except ValidationError as e:
            print(f"Email validation error: {e}")

        except Exception as e:
            print(f"Failed to send email: {e}")