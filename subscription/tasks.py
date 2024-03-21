from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from  .models import *
@shared_task
def check_subs():
    pay=payment.objects.filter(expire_data__lte=datetime.today()-relativedelta(days=1))
    pay.delete()
   

