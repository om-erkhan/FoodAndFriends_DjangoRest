# your_app/utils.py

from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
import random
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def generate_otp():
    return str(random.randint(100000, 999999))


# def send_otp_email(email, otp):
#     subject = "Your OTP Code"
#     message = f"Hi,\n\nYour OTP code is: {otp}\n\nUse this to verify your account."
#     send_mail(subject, message, None, [email])
def send_otp_email(email, otp):
    subject = "Verify your account - Your OTP Code"
    from_email = None
    html_content = render_to_string("otp_template.html", {"otp": otp})
    text_content = f"Hi,\n\nYour OTP code for Food & Friends App is: {otp}\n\nUse this to verify your account."

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return Response(
            {
                "status": {"code": 401, "success": False},
                "data": None,
                "error": "You must be authenticated to access this resource.",
                "message": "Authentication required.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
