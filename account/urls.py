from django.urls import path
from .views import * 

from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns =[
    
    path('send-login-otp/' , LoginOTP.as_view()) , 
    path( 'login-with-otp/' , OtpBasedLogin.as_view()),
    path('send-otp/' , SendOTP.as_view() ),
    path('validate-otp/' , ValidatePhoneOtp.as_view()),
    path('register/' ,Register.as_view()),
    path('passlogin/', UserLoginPassword.as_view()),
    path('chngpass/' ,ChangePasswordView.as_view()),
    path('refreshjwt/',TokenRefreshView.as_view()),
    path('blacklist/' , BlacklistRefreshView.as_view()),
    path('validate-phone-forgot/', ValidatePhoneForgot.as_view()),
	path('validate-forgot-otp/', ValidateForgotOtp.as_view()),
	path('change-forgot-password/', ForgotPasswordChange.as_view()),
    path('change-password/<int:id>/', ChangePasswordView.as_view()),
    path('viewphone/' , ViewPhone.as_view()),
    path("editphone/<int:id>/" , EditPhoneOtp.as_view()),
    
]