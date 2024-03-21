from django.core.mail import send_mail

from django.conf import settings
from .models import PhoneOTP , CustomUser

from .utils import otp_generator


# it will genrate 4 digit otp

def send_otp_via_mail(email ):
    subject='Reservo verification mail'
    otp = str(otp_generator())
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST
    print('email',subject , message  , [email])
    send_mail(subject , message , email_from , [email])
    return otp


