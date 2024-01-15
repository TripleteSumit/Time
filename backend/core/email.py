from django.core.mail import EmailMessage
from django.conf import settings


class EmailUtil:

    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject="Forgot Password OTP",
            body=f"Your forgot password OTP is {data.get('otp')}. Do not share with anyone.",
            from_email=settings.EMAIL_HOST_USER,
            to=[data.get('mail')]
        )
        email.send()
