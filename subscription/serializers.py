from .models import payment 
from rest_framework import serializers

class payment_serlizer(serializers.ModelSerializer):
    class Meta:
        model=payment
        fields='__all__'