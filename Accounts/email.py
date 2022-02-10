from django.core.mail import send_mail
from django.conf import settings

def send_email(message,user_email):
    send_mail(
            'Email Verification OTP',
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )