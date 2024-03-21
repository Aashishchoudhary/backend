from django.contrib import admin

# Register your models here.
from .models import payment


class paymentAdmin(admin.ModelAdmin):
    list_display = ('name','start_date' ,'expire_date' , 'active')

admin.site.register(payment, paymentAdmin)
