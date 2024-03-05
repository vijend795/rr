from django.contrib import admin
from app_property.models import Property 
# Register your models here.







# admin

class PropertyAdmin(admin.ModelAdmin):
    model=Property
    list_display=('custom_id',)
 


admin.site.register(Property,PropertyAdmin)