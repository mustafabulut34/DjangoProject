from django.contrib import admin
from .models import Reservation
# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'total', 'days', 'status']
    list_filter = ['status']
    list_editable = ['status']
    readonly_fields = ['user', 'room', 'name', 'surname',
                       'phone', 'total', 'checkin', 'checkout', 'days', 'ip']
    # can_delete=False


admin.site.register(Reservation, ReservationAdmin)
