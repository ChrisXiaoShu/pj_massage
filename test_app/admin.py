from django.contrib import admin
from test_app.models import Customer, Reservation, MassagerGroup, Massager

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display=('id', 'line_id', 'c_name', 'c_phone','is_black')
    list_filter=('is_black',)
    search_fields=('c_name','c_phone')
    ordering=('id',)


class ReservationAdmin(admin.ModelAdmin):
    list_display=('id', 'customer', 'date', 'c_name', 'c_phone')
    list_filter=('date',)
    search_fields=('customer','c_name')
    ordering=('date',)


class MassagerGroupAdmin(admin.ModelAdmin):
    list_display=('id', 'g_name')
    ordering=('g_name',)

class MassagerAdmin(admin.ModelAdmin):
    list_display=('id', 'm_name', 'massagergroup')
    list_filter=('massagergroup',)
    search_fields=('m_name','massagergroup')
    ordering=('massagergroup',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(MassagerGroup, MassagerGroupAdmin)
admin.site.register(Massager, MassagerAdmin)
