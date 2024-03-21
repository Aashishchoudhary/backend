from celery import shared_task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from  .models import *

@shared_task
def delete_closed_room(self , request):
    time = datetime.now()-relativedelta(hours=24)
    room = student_data.objects.filter(expires_at__lte=time)
    room.delete()

@shared_task
def delete_unverified_image(self , request):
    image_model=image_data.objects.filter(verified=False)
    image_model.delete()

@shared_task
def delete_signature(self):
    time = datetime.now()-relativedelta(minutes=30)
    sign = Signature.objects.filter(expires_at__lte=time)
    sign.delete()
    