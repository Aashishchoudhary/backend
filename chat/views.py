from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
# Create your views here.
from .models import  Signature

from .chustom_perm import check_perm

from alpha.models import LibrarySeat ,Library
from alpha.serializer import SeatResSerializer , HalfTimerSerlizer , ExtraStudentSerailzer ,LibrarySeatSerializer

import random 
import string
from datetime import datetime 
from dateutil.relativedelta import relativedelta


class sign_genration(APIView):
    permission_classes=[IsAuthenticated]
    def get(self , request):
        user =request.user.id
        sign= ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
          # Implement your signature generation
        print('user' , user)
        Signature.objects.create(user_id=user, sign=sign)
        return Response({'user':user,'sign':sign} , status=200)




class chat_message(APIView):
    permission_classes=[AllowAny]
    def get(self , request):
        return render (request , 'main.html')
    
class half_chat_message(APIView):
    permission_classes=[AllowAny]
    def get(self , request):
        return render (request , 'half.html')

 

class add_seat_reservation_view(APIView):
    permission_classes=[AllowAny]
    def post(self, request, lib_id, id ,user_id , sign):
        if check_perm(user_id , sign):
            seat = LibrarySeat.objects.filter(lib_id=lib_id, seat_num=id)
            seat_serlizer = LibrarySeatSerializer(seat, many=True)
            seatid = seat_serlizer.data[0]['id']
            data = {
                "reserved_seat": seatid,
                "name": request.data.get('name'),
                'mobile_number': request.data.get('mobile_number'),
                'adharcard': request.data.get('adharcard'),
                'photo': request.data.get('photo'),
                'adress': request.data.get('adress'),
                'gender': request.data.get('gender'),
                'dob': request.data.get('dob')
            }
            ser=SeatResSerializer(data=data)
            print(data , ser.is_valid())
            if ser.is_valid():
                ser.save()
                sinn = Signature.objects.filter(user= user_id, sign= sign )
                sinn.delete()
                return Response({'data':"data saved"} , status=200)
            return Response({'data':"something went wrong"},status=400)
        else:
            return Response({'data':"Time limit excessed"} ,status=400)



class half_time_add(APIView):
    permission_classes=[AllowAny]
    def post(self, request, id ,user_id , sign): 
        if check_perm(user_id , sign):      
            lib = Library.objects.filter( id=id)     
            if lib.count()<25:
                data = {'lib_name': id,
                         "name": request.data.get('name'),                   
                        'mobile_number': request.data.get('mobile_number'),
                        'adharcard': request.data.get('adharcard'),
                        'photo': request.data.get('photo'),
                        'adress': request.data.get('adress'),
                        'gender': request.data.get('gender'),
                        'dob': request.data.get('dob') 
                        }
                ser = HalfTimerSerlizer(data=data)
                print(data , ser.is_valid())
                if ser.is_valid():
                    ser.save()
                    sinn = Signature.objects.filter(user= user_id, sign= sign )
                    sinn.delete()
                    return Response(status=200)
                return Response({'data':"something went wrong"},status=400)
            return Response({'data':"can not add more than 25"},status=400)
        else:
            return Response({'data':"Time limit excessed"},status=400)


class add_extra(APIView):
    permission_classes=[AllowAny]
    def post(self, request, id ,user_id , sign): 
        print(check_perm(user_id , sign))
        if check_perm(user_id , sign):
            print('ddd')
            lib = Library.objects.filter(id=id)
            if lib.count()<25:
                data = {'lib': id, "name": request.data.get('name'),
                        "amount": request.data.get('amount'),
                        'mobile_number': request.data.get('mobile_number'),
                        'start_date': request.data.get('start_date'),
                        'end_date': request.data.get('end_date'),
                        'adharcard': request.data.get('adharcard'),
                        'photo': request.data.get('photo'),
                        'adress': request.data.get('adress'),
                        'gender': request.data.get('gender'),
                        'dob': request.data.get('dob')}
                ser = ExtraStudentSerailzer(data=data)
                print(data ,ser.is_valid())
                if ser.is_valid():
                    ser.save()
                    sinn = Signature.objects.filter(user= user_id, sign= sign )
                    sinn.delete()
                    return Response({'data':"data saved"},status=200)
                return Response({'data':"something went wrong"},status=400)
            return Response({'data':"can not add more than 25"} ,status=400)
        else:
            return Response({'data':"Time limit excessed"} ,status=400)