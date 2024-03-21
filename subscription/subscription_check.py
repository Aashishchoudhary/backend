from .models import payment
from rest_framework.response import Response
from .serializers import payment_serlizer
from rest_framework.permissions import BasePermission
from datetime import datetime ,timedelta
class check_subscription(BasePermission):   
        message={'details':'dont have subscription','status':468}
        def has_permission(self , request ,view):
             user= payment.objects.filter(name=request.user.id)
             if user.exists(): 
                ser=payment_serlizer(user , many=True).data
                date_str= ser[0]['expire_date']
                date = datetime.strptime(date_str, '%Y-%m-%d')
                if ser[0]['active'] and date > datetime.now()-timedelta(1):
                   print('true')
                   return True
                else:
                     print('false')
                    
                     return False
             else:
                  print('f2')
                  return False
        

