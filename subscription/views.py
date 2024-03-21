import razorpay

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  ,AllowAny
from .serializers import payment_serlizer
from dateutil.relativedelta import relativedelta
from datetime import date ,datetime
# Create your views here.


import math
from account.models import CustomUser
from account.serializer import CustomUserSerlizer
from alpha.models import Library
from alpha.serializer import LibrarySerializer

from account.models import CustomUser 
from alpha.models import AmountCollection
from alpha.serializer import AmountCollectionSerailzer
from .models import payment 
from .serializers import payment_serlizer
from .subscription_check import check_subscription

from dotenv import load_dotenv

import os
load_dotenv()
client = razorpay.Client(auth=(os.environ['key'], os.environ['secret']))


class paymentApi(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        user = CustomUser.objects.filter(id=user_id)
        user_serliazer = CustomUserSerlizer(user , many=True)
        print('type ',user_serliazer.data[0]['username'])
        library=Library.objects.filter(owner_id=user_id )              
        library_serlizer=LibrarySerializer(library , many=True)
        result_data=[]
        total_amount=0
        
        for i in range(len(library_serlizer.data)):

            amount_collection_model_data= AmountCollection.objects.filter(library_id=library_serlizer.data[i]['id'])
            amount_collecttion_serlised_data=AmountCollectionSerailzer(amount_collection_model_data , many=True)
            total_amount +=amount_collecttion_serlised_data.data[1]['amount']
            result_data.append(amount_collecttion_serlised_data.data)
        
        amount = math.ceil(total_amount*100*0.0011)
        if amount<7000:
            # amount =7000
            
            print('amount payable ' , amount)
            dd = client.order.create({
                "amount":7000 ,
                "currency": "INR",
                "receipt": "receipt#1",
                "partial_payment": False,
                "notes": {
                    "key1": user_serliazer.data[0]['username'],
                    "key2": "value2"
                },
    
            })
            print('dd',dd)
            return Response(dd, status=200)
        else:
            dd = client.order.create({
                "amount": amount,
                "currency": "INR",
                "receipt": "receipt#1",
                "partial_payment": False,
                "notes": {
                    "key1": user_serliazer.data[0]['username'],
                    "key2": "value2"
                },
    
            })
            print(dd)
            return Response(dd, status=200)


class addPaymentModel(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):        
        oreder_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')
        ff = client.utility.verify_payment_signature({
            'razorpay_order_id': oreder_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        if ff:
            name = request.user.id
          
            expiry_date = date.today() + relativedelta(months=1)            
            data = {'name': name, 'expire_date': expiry_date ,'active':True}
            print(expiry_date ,type(expiry_date))
            ser = payment_serlizer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(f'you have subscriotion till date{expiry_date} ', status=200)
        return Response(ser.errors, status=400)



class paymentApi_3months(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        user_id = request.user.id
        
        user = CustomUser.objects.filter(id=user_id)
        user_serliazer = CustomUserSerlizer(user , many=True)
        print('type ',user_serliazer.data[0]['username'])
        library=Library.objects.filter(owner_id=user_id  )              
        library_serlizer=LibrarySerializer(library , many=True)
        result_data=[]
        total_amount=0
        
        for i in range(len(library_serlizer.data)):

            amount_collection_model_data= AmountCollection.objects.filter(library_id=library_serlizer.data[i]['id'])
            amount_collecttion_serlised_data=AmountCollectionSerailzer(amount_collection_model_data , many=True)
            total_amount +=amount_collecttion_serlised_data.data[1]['amount']
            result_data.append(amount_collecttion_serlised_data.data)
        
        amount = math.ceil(total_amount*100*3*0.0011)
        if amount<7000:
            # amount =7000
            
            print('amount payable ' , amount)
            dd = client.order.create({
                "amount":21000 ,
                "currency": "INR",
                "receipt": "receipt#1",
                "partial_payment": False,
                "notes": {
                    "key1": user_serliazer.data[0]['username'],
                    "key2": "value2"
                },
    
            })
            print('dd',dd)
            return Response(dd, status=200)
        else:
            dd = client.order.create({
                "amount": amount,
                "currency": "INR",
                "receipt": "receipt#1",
                "partial_payment": False,
                "notes": {
                    "key1": user_serliazer.data[0]['username'],
                    "key2": "value2"
                },
    
            })
            print(dd)
            return Response(dd, status=200)


class addPaymentModel_3months(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):        
        oreder_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')
        ff = client.utility.verify_payment_signature({
            'razorpay_order_id': oreder_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        if ff:
            name = request.user.id
          
            expiry_date = date.today() + relativedelta(months=3)

           
            data = {'name': name, 'expire_date': expiry_date ,'active':True}

            ser = payment_serlizer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(f'you have subscriotion till date{expiry_date} ', status=200)
        return Response(ser.errors, status=400)


class viewSubscription(APIView):
    permission_classes=[IsAuthenticated ,check_subscription ]
    def get(self , request):
        user_id = request.user.id
        subscription = payment.objects.filter(name = user_id)
        subs_serlizer=payment_serlizer(subscription , many=True)
        return Response(subs_serlizer.data)
    



class subscribed_user_one_month_model(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request):     
        user_id = request.user.id
        subscription = payment.objects.get(name = user_id)
        subs_serlizer=payment_serlizer(subscription) 
        expire_date_str=subs_serlizer.data['expire_date']  
        expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d')

        oreder_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')
        ff = client.utility.verify_payment_signature({
            'razorpay_order_id': oreder_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        if ff:
            
          
            expiry_date = datetime.date(expire_date) + relativedelta(months=1)
           
            data = { 'expire_date': expiry_date}

            ser = payment_serlizer(subscription,data=data,partial=True)
            if ser.is_valid():
                ser.save()
                return Response(f'you have subscriotion till date{expiry_date} ', status=200)
        return Response(ser.errors, status=400)





class subscribed_user_3months_model(APIView):
    permission_classes=[IsAuthenticated ,check_subscription ]
    def patch(self, request):   
        user_id = request.user.id
        subscription = payment.objects.get(name = user_id)
        subs_serlizer=payment_serlizer(subscription) 
        print(subs_serlizer)
        expire_date_str=subs_serlizer.data['expire_date']  
        print(expire_date_str)
        expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d')     
        oreder_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')
        ff = client.utility.verify_payment_signature({
            'razorpay_order_id': oreder_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        if ff:
            
          
            expiry_date = datetime.date(expire_date)+ relativedelta(months=3)
           
            data = {'expire_date': expiry_date }

            ser = payment_serlizer(subscription,data=data,partial=True)
            if ser.is_valid():
                ser.save()
                return Response(f'you have subscriotion till date{expiry_date} ', status=200)
        return Response(ser.errors, status=400)


    
