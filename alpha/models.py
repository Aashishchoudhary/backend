
from django.db import models
from django.db.models.signals import post_save  ,pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

def upload_path( instance,filname):
    return '/'.join(['covers',filname])

class Library(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    facilty=models.CharField(max_length=1000 ,null=True ,blank=True)
    locality=models.CharField(max_length=100,null=True ,blank=True)
    city=models.CharField(max_length=100,null=True ,blank=True)
    district=models.CharField(max_length=100,null=True ,blank=True)
    pincode=models.IntegerField(null=True ,blank=True)
    imageOne=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    imageTwo=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    imageThree=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    imageFour=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    imageFive=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    imageSix=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    imageSeven=models.ImageField(upload_to=upload_path,  null=True , blank=True )

    price=models.IntegerField(null=True ,blank=True)
    mobile_number=models.CharField(max_length=12)
    whatsapp_number=models.CharField(max_length=12,null=True ,blank=True)
    longitude=models.FloatField(null=True ,blank=True)
    latitude=models.FloatField( null=True , blank=True)
    total_seat = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(500),
            MinValueValidator(1)
        ])
    

    def __str__(self):
        return f'{self.name}'


@receiver(post_save, sender=Library)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for x in range(instance.total_seat):
            seat = LibrarySeat.objects.create(lib=instance, seat_num=x+1)
            seat.save()


# Connect the signal receiver function



class LibrarySeat(models.Model):
    
    lib = models.ForeignKey(Library, on_delete=models.CASCADE)
    
    seat_num = models.IntegerField()
    booked=models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.lib.name} - Seat {self.seat_num}"



class SeatReservation(models.Model):    
    reserved_seat =models.OneToOneField(LibrarySeat ,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    mobile_number=models.CharField(max_length=12) 
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    created_at = models.DateField(auto_now_add=True ,null=True)
    updated_at = models.DateField(auto_now=True ,null=True)
    amount = models.IntegerField(null=True)
    adharcard=models.FileField( null=True ,blank=True)
    photo=models.FileField(blank=True , null=True)
    dob=models.DateField(null=True)
    adress=models.CharField(max_length=300,null=True ,blank=True)
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES)


    def __str__(self):
         return f"{self.reserved_seat} - {self.name}"




class DeletedHistory(models.Model):
    owner=models.CharField(max_length=100)
    reserved_seat =models.CharField(max_length=100 ,null=True  , blank=True)
    name=models.CharField(max_length=100,null=True)
    amount=models.IntegerField(null=True  , blank=True)
    
    deleted_at = models.DateField(auto_now_add=True ,null=True)
    created_on= models.CharField(max_length=40 ,null=True)
    
    mobile_number=models.CharField(max_length=12 ,null=True) 
    start_date=models.DateField(null=True)    
    end_date=models.DateField(null=True)
    adharcard=models.ImageField(upload_to=upload_path ,null=True  , blank=True)
    photo=models.ImageField(upload_to=upload_path ,blank=True , null=True)
    dob=models.CharField(max_length=50,null=True)
    adress=models.CharField(max_length=300,null=True ,blank=True)
    
    
    gender = models.CharField(max_length=10)
    





@receiver(pre_delete, sender=SeatReservation)
def delete_seats(sender, instance, **kwargs):
  
    delete_res = DeletedHistory(owner=instance.reserved_seat.lib.id,reserved_seat=instance.reserved_seat,created_on=instance.created_at,
                                amount=instance.amount ,  
    name=instance.name ,mobile_number=instance.mobile_number ,start_date=instance.start_date , end_date=instance.end_date , adharcard=instance.adharcard , photo=instance.photo,dob=instance.dob , adress=instance.adress , gender=instance.gender
    )
    delete_res.save()
    instance.reserved_seat.booked = False
    instance.reserved_seat.save()


@receiver(post_save, sender=SeatReservation)
def create_seats(sender, instance, created, **kwargs):            
    if created:        
        instance.reserved_seat.booked = True        
        instance.reserved_seat.save()



# for half timers
class HalfTimer(models.Model):
    lib_name=models.ForeignKey(Library , on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True,blank=True)
    mobile_number=models.CharField(max_length=12 ,null=True,blank=True) 
    amount=models.IntegerField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True ,null=True)
    updated_at = models.DateField(auto_now=True ,null=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    adharcard=models.ImageField(upload_to=upload_path ,blank=True,  null=True)
    photo=models.ImageField(upload_to=upload_path ,blank=True , null=True)
    dob=models.DateField(null=True,blank=True)
    adress=models.CharField(max_length=300,null=True ,blank=True)
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES , null=True , blank=True)


@receiver(pre_delete ,sender=HalfTimer)
def delete_halfTimer(sender , instance ,**kwargs):
    del_his=DeletedHistory(owner=instance.lib_name.id,
                           reserved_seat=instance.lib_name,
    name=instance.name ,mobile_number=instance.mobile_number ,amount=instance.amount,start_date=instance.start_date ,created_on=instance.created_at, end_date=instance.end_date  , adharcard=instance.adharcard , photo=instance.photo,dob=instance.dob , adress=instance.adress , gender=instance.gender
    )
    del_his.save()


# for extra persons

class ExtraStudent(models.Model):
    lib=models.ForeignKey(Library , on_delete=models.CASCADE)
    name=models.CharField(max_length=100 ,null=True,blank=True)
    mobile_number=models.CharField(max_length=12,null=True,blank=True) 
    amount=models.IntegerField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True ,null=True)
    updated_at = models.DateField(auto_now=True ,null=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    adharcard=models.ImageField(upload_to=upload_path ,blank=True,  null=True)
    photo=models.ImageField(upload_to=upload_path ,blank=True , null=True)
    dob=models.DateField(null=True,blank=True)
    adress=models.CharField(max_length=300,null=True ,blank=True)
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES , null=True , blank=True)



@receiver(pre_delete ,sender=ExtraStudent)
def delete_halfTimer(sender , instance ,**kwargs):
    del_his=DeletedHistory(owner=instance.lib.id, reserved_seat=instance.lib,
    name=instance.name ,mobile_number=instance.mobile_number ,created_on=instance.created_at,amount=instance.amount ,start_date=instance.start_date , end_date=instance.end_date , adharcard=instance.adharcard ,  photo=instance.photo ,dob=instance.dob , adress=instance.adress , gender=instance.gender
    )
    del_his.save()


#collection for whole month

class AmountCollection(models.Model):
    library= models.ForeignKey(Library , on_delete=models.CASCADE)
    collection_month=models.DateField(auto_now_add=True ,null=True)
    amount=models.IntegerField()
    cost=models.TextField(null=True ,blank=True)
    finalCost=models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-collection_month',)