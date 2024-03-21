from django.contrib import admin

# Register your models here.

from .models import *


class NameAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(student_data, NameAdmin)

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('sign',)

admin.site.register(Signature, SignatureAdmin)


class imgAdmin(admin.ModelAdmin):
    list_display = ('uuid',)

admin.site.register(image_data, imgAdmin)
