from django.contrib import admin,messages
from django.db import IntegrityError
from django.utils.translation import ngettext
from django.urls import reverse
from django.http import HttpResponseRedirect

# Register your models here.


from app_address.models import Address,City,State,Country,Locality,Plot,Building,LocalityType,SubLocality, Area

# Inline 
class PlotInline(admin.StackedInline):
    model=Plot
    extra=1

class LocalityInline(admin.StackedInline):
    model=Locality
    extra=1



class CityInline(admin.StackedInline):
    model=City
    extra=1
class StateInline(admin.StackedInline):
    model=State
    extra=1



# admin site 
class CountryAdmin(admin.ModelAdmin):
    list_display=('custom_id','country_name','country_mobile_code',)
    inlines=[StateInline]

class StateAdmin(admin.ModelAdmin):
    list_display=('custom_id','state_name','country',)
    inlines=[CityInline]

class CityAdmin(admin.ModelAdmin):
    list_display=('custom_id','city_name','state')
    inlines=[LocalityInline]

class LocalityTypeAdmin(admin.ModelAdmin):
    list_display=('custom_id','locality_type_name')
    actions = ['duplicate_selected']
# 
    # def duplicate_selected(self, request, queryset):
    #     for obj in queryset:
    #         try:
    #             # Create a new object with the same values
    #             new_obj = self.model.objects.create(**{field.name: getattr(obj, field.name) for field in self.model._meta.fields if field.name != 'id'})

    #             # Redirect to the edit view for the new object
    #             change_url = reverse('admin:%s_%s_change' % (new_obj._meta.app_label,  new_obj._meta.model_name), args=[new_obj.id], current_app=self.admin_site.name)
    #             return HttpResponseRedirect(change_url)
    #         except Exception as e:
    #             messages.error(request, f"Failed to duplicate {obj}: {str(e)}")

    #     self.message_user(request, ngettext(
    #         '%d object was successfully duplicated.',
    #         '%d objects were successfully duplicated.',
    #         len(queryset),
    #     ) % len(queryset), messages.SUCCESS)

    #     return HttpResponseRedirect(request.get_full_path())

    # duplicate_selected.short_description = "Duplicate selected %(verbose_name_plural)s"


    


    

class SubLocalityAdmin(admin.ModelAdmin):
    list_display=('custom_id','sub_locality_name','locality')

class SubLocalityInline(admin.StackedInline):
    model=SubLocality
    extra=1

class LocalityAdmin(admin.ModelAdmin):
    list_display=('custom_id','locality_type','locality_name','display_sub_locality','city','pin_code')
    inlines=[SubLocalityInline]
    def display_sub_locality(self,obj):
        return ", ".join(str(sub_localities) for sub_localities in obj.sub_localities.all())
    
    display_sub_locality.short_description="Sub Localities"

class AreaAdmin(admin.ModelAdmin):
    list_display=('custom_id','area_name',)


class PlotAdmin(admin.ModelAdmin):
    list_display=('custom_id','plot_no','building')

    # def display_localities(self,obj):
    #     return ", ".join(str(locality)for locality in obj.localities.all())
    
    # display_localities.short_description="Localities"



class BuildingAdmin(admin.ModelAdmin):
    list_display=('custom_id','building_name')
    inlines=[PlotInline]

class AddressAdmin(admin.ModelAdmin):
    list_display=('custom_id','unit_no','floor','building')
    



admin.site.register(Country,CountryAdmin)
admin.site.register(State,StateAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Locality,LocalityAdmin)
admin.site.register(SubLocality,SubLocalityAdmin)
admin.site.register(LocalityType,LocalityTypeAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Plot,PlotAdmin)
admin.site.register(Building,BuildingAdmin)
admin.site.register(Address,AddressAdmin)

