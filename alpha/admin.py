from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Library , LibrarySeat ,SeatReservation , ExtraStudent , HalfTimer , DeletedHistory ,AmountCollection )
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]





