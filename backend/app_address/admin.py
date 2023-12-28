from django.contrib import admin,messages
from django.db import IntegrityError
from django.utils.translation import ngettext
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db import models
from .forms import DynamicRelationAreaLocalityForm

# Register your models here.


from app_address.models import Address,City,State,Country,Locality,Plot,Building,LocalityType,SubLocality, Area, DynamicRelationAreaLocality

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


   

class SubLocalityAdmin(admin.ModelAdmin):
    list_display=('custom_id','sub_locality_name','locality')

class SubLocalityInline(admin.StackedInline):
    model=SubLocality
    extra=1
class LocalityInline(admin.StackedInline):
    model=Locality
    extra=1

class LocalityAdmin(admin.ModelAdmin):
    list_display=('custom_id','locality_type','locality_name','display_sub_locality','city')
    inlines=[SubLocalityInline]
    def display_sub_locality(self,obj):
        # return ",\n ".join(str(sub_localities) for sub_localities in obj.sub_localities.all())
        sub_localities = obj.sub_localities.all()
        if sub_localities:
            return mark_safe("<br>".join(str(sub_locality) for sub_locality in sub_localities))
        return ""
       
    
    display_sub_locality.short_description="Sub Localities"

class DynamicRelationAreaLocalityAdmin(admin.ModelAdmin):
    form = DynamicRelationAreaLocalityForm

    def save_model(self, request, obj, form, change):
        # Set the locality_type based on your logic (e.g., get it from the request or other fields)
        obj.locality_type = form.cleaned_data['locality_type']
        obj.save()

class DynamicRelationAreaLocalityInline(admin.TabularInline):
    model = DynamicRelationAreaLocality
    form=DynamicRelationAreaLocalityForm
    extra=1

class AreaAdmin(admin.ModelAdmin):
    form = DynamicRelationAreaLocalityForm
    list_display=('custom_id','pin_code','display_localities')
    inlines=[DynamicRelationAreaLocalityInline]

    def display_localities(self, obj):
        localities = DynamicRelationAreaLocality.objects.filter(area=obj).order_by('locality_type__locality_type_name')
        if localities:
            return mark_safe("<br>".join(f"{relation.locality_type} - {relation.locality}" for relation in localities))
        return ""
    display_localities.short_description = "Localities"
    
    


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
admin.site.register(DynamicRelationAreaLocality,DynamicRelationAreaLocalityAdmin)

