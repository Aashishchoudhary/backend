from rest_framework import serializers
from .models import Library , LibrarySeat , SeatReservation , DeletedHistory ,HalfTimer ,ExtraStudent ,AmountCollection 


 

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model=Library
        fields='__all__'


class LibrarySeatSerializer(serializers.ModelSerializer):
    class Meta:
        model=LibrarySeat
        fields='__all__'


class SeatResSerializer(serializers.ModelSerializer):
    class Meta:
        model=SeatReservation
        fields='__all__'

class DelteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=DeletedHistory
        fields='__all__'

class HalfTimerSerlizer(serializers.ModelSerializer):
    class Meta:
        model=HalfTimer
        fields='__all__'


class ExtraStudentSerailzer(serializers.ModelSerializer):
    class Meta:
        model=ExtraStudent
        fields='__all__'


class AmountCollectionSerailzer(serializers.ModelSerializer):
    class Meta:
        model=AmountCollection
        fields='__all__'