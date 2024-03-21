from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUserManager(BaseUserManager ):
    def create_user(self,username ,email, password ,**extra_fields):
        if not username and not email:
            raise ValueError("User must enter username number and Email")
        
        email = self.normalize_email(email)
        user=self.model(username=username , email=email ,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username,email,password, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email,username, password, **extra_fields)
    

class CustomUser(AbstractUser):
   
    
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    username =models.CharField(validators=[phone_regex], max_length=13, unique=True)
    email = models.EmailField(unique=True)
    standard=models.CharField(max_length=3 , blank=True , null=True)
    is_active      =models.BooleanField(default=True)
    is_staff       = models.BooleanField(default=False)
    is_admin       = models.BooleanField(default=False)

    timestamp   = models.DateTimeField(auto_now_add=True)

    objects=CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' ]

    def __str__(self):
        return self.username


class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")

    # regex to validate mobile numbers
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True , null=True)
    email       = models.EmailField(unique = True ,null=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')
    created_at= models.DateTimeField(auto_now = True)
    otp_valid = models.BooleanField(default=False)
    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save , sender=PhoneOTP)
def otp_expiration(sender, instance, created, **kwargs):
    if instance.otp_valid==True:
        instance.otp_valid = False
        instance.save()


