from django.contrib import admin
from app_property.models import Property ,SubProperty,SubPropertyType
# Register your models here.
class SubPropertyInline(admin.StackedInline):
    model=SubProperty
    extra=1





# admin

class PropertyAdmin(admin.ModelAdmin):
    model=Property
    list_display=('custom_id',)
    inlines=[SubPropertyInline]

class SubPropertyAdmin(admin.ModelAdmin):
    model=SubProperty
    list_display=('custom_id',)
 
class SubPropertyTypeAdmin(admin.ModelAdmin):
    model=SubPropertyType
    list_display=('custom_id',)
 


admin.site.register(Property,PropertyAdmin)
admin.site.register(SubProperty,SubPropertyAdmin)
admin.site.register(SubPropertyType,SubPropertyTypeAdmin)