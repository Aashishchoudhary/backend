from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from .models import PhoneOTP ,CustomUser
User = get_user_model()



class CreateUserSerialzier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username' ,'email','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class ChangePasswordSerializer(serializers.Serializer):
    # model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    refresh = serializers.CharField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(required=True)

    


class PhoneOtpSerlizer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields='__all__'


class CustomUserSerlizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields='__all__'


class SendRegisterOtpSerliazer(serializers.Serializer):
    phone=serializers.IntegerField()
    email=serializers.EmailField()

class ValidateRegisterOtp(serializers.Serializer):
    phone=serializers.CharField(max_length=30)
    email=serializers.EmailField()
    otp=serializers.IntegerField()
