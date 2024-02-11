from django.contrib import admin
from app_property.models import Property ,PropertyAddressRelationship
# Register your models here.


# inlines 
class PropertyAddressRelationshipInline(admin.TabularInline):
    model=PropertyAddressRelationship
    extra=1




# admin

class PropertyAdmin(admin.ModelAdmin):
    model=Property
    list_display=('custom_id','area_in_sq_ft','property_for','property_use','property_type')
    inlines=[PropertyAddressRelationshipInline]


admin.site.register(Property,PropertyAdmin)