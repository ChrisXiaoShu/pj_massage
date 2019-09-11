from django.contrib import admin
from test_app.models import Customer, Reservation, MasterGroup, Master

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display=('line_id', 'name', 'phone','is_black')
    list_filter=('is_black',)
    search_fields=('name','phone')
    ordering=('line_id',)


class ReservationAdmin(admin.ModelAdmin):
    list_display=('id', 'customer', 'master', 'datetime', 'name', 'phone', 'has_remind')
    list_filter=('datetime',)
    search_fields=('customer','name')
    ordering=('datetime',)


class MasterGroupAdmin(admin.ModelAdmin):
    list_display=('id', 'name')
    ordering=('name',)

class MasterAdmin(admin.ModelAdmin):
    list_display=('master_id', 'group', 'name', 'work_type')
    list_filter=('group',)
    search_fields=('master_id','name')
    ordering=('group',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(MasterGroup, MasterGroupAdmin)
admin.site.register(Master, MasterAdmin)
