from django.db import models
from account.models import CustomUser
# Create your models here.
from django.db.models.signals import post_save
from datetime import date
from dateutil.relativedelta import relativedelta
class payment(models.Model):
    name= models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    start_date=models.DateField(auto_now_add=True)
    expire_date=models.DateField(null=True)
    active=models.BooleanField(default=True)





    

from django.dispatch import receiver
@receiver(post_save , sender=CustomUser)
def add_subs(sender , instance,created, **kwargs):
    if created:
      print(instance)
      today=date.today()+ relativedelta(days=80)
      subs= payment(name=instance ,expire_date=today)
      subs.save()
