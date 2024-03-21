from django.db import models
from account.models import CustomUser

# Create your models here.


class student_data(models.Model):
    name = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50,null=True)
    mobile_number = models.CharField(max_length=12,null=True)
    uuid=models.CharField(max_length=20 , null=True)
    dob = models.DateField(null=True)
    adharcard =  models.CharField(max_length=50,null=True)
    photo = models.CharField(max_length=50,null=True)
    stream = models.CharField(max_length=50,null=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES,null=True)
    expires_at= models.DateTimeField(auto_now_add=True)
    submitted=models.BooleanField(default=False)



class image_data(models.Model):
    uuid=models.CharField(max_length=100 ,null = True)
    verified = models.BooleanField(default=False)
    photo=models.ImageField(null=True)
    adharcard=models.ImageField(null=True)



class Signature(models.Model):
    user = models.ForeignKey(CustomUser,on_delete =models.CASCADE)
    sign=models.CharField(max_length=64, unique=True ,null=True)
    expires_at= models.DateTimeField(auto_now_add=True)



from django.dispatch import receiver
from django.db.models.signals import post_delete



# By adding 'Car' as 'sender' argument we only receive signals from that model
@receiver(post_delete, sender=image_data)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    # ref is the name of the field file of the Car model
    # replace with name of your file field
    instance.photo.delete()
    instance.adharcard.delete()