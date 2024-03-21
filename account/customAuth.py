from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend
from .models import PhoneOTP
from django.db.models import Q
User = get_user_model()

class CustomAuthentication(ModelBackend):
    def authenticate(self, request, username, otp):
        OTP = PhoneOTP.objects.filter(Q(phone=username)|Q(email=username)).first()
        print('otp',username,OTP.otp ,'ff',otp)
        
        if  str(otp) != OTP.otp:
            raise AuthenticationFailed('Invalid OTP')

        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            print(user)
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed('User does not exist')



class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
     
        try:
            print('username ',username)
            user = User.objects.get(Q(username=username)|Q(email=username))
            print(user.password , password)
            if user.check_password(password):
              
              return user
            else:
                raise ValueError("password incorrect")
        except :
            raise ValueError('User does not exist')

    