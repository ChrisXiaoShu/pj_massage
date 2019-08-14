from django.contrib import admin
from test_app.models import customer

# Register your models here.
class customerAdmin(admin.ModelAdmin):
    list_display=('id', 'cName', 'cPhone','isBlack')
    list_filter=('isBlack',)
    search_fields=('cName','cPhone')
    ordering=('id',)


admin.site.register(customer, customerAdmin)
