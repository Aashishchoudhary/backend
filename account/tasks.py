from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from  .models import *
from .utils import six_digit_otp_genrator

@shared_task
def otp_expire():
    time = datetime.now() - relativedelta(minutes=10)
    PhoneOTP.objects.filter(otp_valid=False ,created_at__lte=time).update(otp_valid=True , 
    otp=six_digit_otp_genrator()) 