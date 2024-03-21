from rest_framework import serializers

from .models import image_data , student_data ,Signature


class image_data_serlizer(serializers.ModelSerializer):
    class Meta:
        model=image_data
        fields="__all__"

class student_data_serlizer(serializers.ModelSerializer):
    class Meta:
        model=student_data
        fields="__all__"

class signature_Serlizer(serializers.ModelSerializer):
    class Meta:
        model=Signature
        fields="__all__"

