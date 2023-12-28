from django.contrib import admin,messages
from django.db import IntegrityError
from django.utils.translation import ngettext
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db import models
from .forms import DynamicRelationAreaLocalityForm

# Register your models here.


from app_address.models import Address,City,State,Country,Locality,Plot,Building,LocalityType, Area, DynamicRelationAreaLocality,Street,Landmark,StreetPlotRelationship, LandmarkPlotRelationship

# Inline 
class PlotInline(admin.TabularInline):
    model=Plot
    extra=1

class LocalityInline(admin.TabularInline):
    model=Locality
    extra=1

class DynamicRelationAreaLocalityInline(admin.TabularInline):
    model = DynamicRelationAreaLocality
    form=DynamicRelationAreaLocalityForm
    extra=1
class StreetPlotRelationshipInline(admin.TabularInline):
    model = StreetPlotRelationship
    extra = 1

class LandmarkPlotRelationshipInline(admin.TabularInline):
    model = LandmarkPlotRelationship
    extra = 1

class CityInline(admin.TabularInline):
    model=City
    extra=1
class StateInline(admin.TabularInline):
    model=State
    extra=1
class LocalityInline(admin.TabularInline):
    model=Locality
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


   



class LocalityAdmin(admin.ModelAdmin):
    list_display=('custom_id','locality_type','sub_locality_name','locality_name','city')


class DynamicRelationAreaLocalityAdmin(admin.ModelAdmin):
    form = DynamicRelationAreaLocalityForm

    def save_model(self, request, obj, form, change):
        # Set the locality_type based on your logic (e.g., get it from the request or other fields)
        obj.locality_type = form.cleaned_data['locality_type']
        obj.save()



class AreaAdmin(admin.ModelAdmin):
    form = DynamicRelationAreaLocalityForm
    list_display=('custom_id','pin_code','display_localities')
    inlines=[DynamicRelationAreaLocalityInline,PlotInline]

    def display_localities(self, obj):
        localities = DynamicRelationAreaLocality.objects.filter(area=obj).order_by('locality_type__locality_type_name')
        if localities:
            return mark_safe("<br>".join(f"{relation.locality_type} - {relation.locality}" for relation in localities))
        return ""
    display_localities.short_description = "Localities"
    
class StreetAdmin(admin.ModelAdmin):
    list_display=('custom_id','street_name','get_plot_numbers')   
    inlines=[StreetPlotRelationshipInline]
    
    def get_plot_numbers(self, obj):
        plot_numbers = obj.street_plot_relationships.all().order_by('plot__plot_no')
        # return ", ".join(str(relationship.plot.plot_no) for relationship in plot_numbers)
        if plot_numbers:
            return mark_safe("<br>".join(str(relationship.plot.plot_no) for relationship in plot_numbers))
        return ""


    get_plot_numbers.short_description = 'Plot Numbers'

class LandmarkAdmin(admin.ModelAdmin):
    list_display=('custom_id','landmark_name','get_plot_numbers')  
    inlines=[LandmarkPlotRelationshipInline] 
    def get_plot_numbers(self, obj):
        plot_numbers = obj.landmark_plot_relationships.all().order_by('plot__plot_no')
        # return ", ".join(str(relationship.plot.plot_no) for relationship in plot_numbers)
        if plot_numbers:
            return mark_safe("<br>".join(str(relationship.plot.plot_no) for relationship in plot_numbers))
        return ""

    get_plot_numbers.short_description = 'Plot Numbers'



class PlotAdmin(admin.ModelAdmin):
    list_display=('custom_id','plot_no','building','area','get_all_streets','get_all_landmark')
    inlines=[StreetPlotRelationshipInline,LandmarkPlotRelationshipInline]

    def get_all_streets(self, obj):
        street_relationships = obj.street_plot_relationships.all().order_by('street__street_name')
        # return ", ".join(f"{relationship.street.street_name} (Order: {relationship.order})" for relationship in street_relationships)
        if street_relationships:
            return mark_safe("<br>".join(str(relationship.street.street_name)for relationship in street_relationships))
        return ""

    def get_all_landmark(self, obj):
        landmark_relationships = obj.landmark_plot_relationships.all().order_by('landmark__landmark_name')
        # return ", ".join(f"{relationship.landmark.landmark_name} (Order: {relationship.order})" for relationship in landmark_relationships)
        if landmark_relationships:
            return mark_safe("<br>".join(str(relationship.landmark.landmark_name)for relationship in landmark_relationships))
        return ""

    get_all_streets.short_description="Streets"
    get_all_landmark.short_description="Landmark"



class BuildingAdmin(admin.ModelAdmin):
    list_display=('custom_id','building_name')
    inlines=[PlotInline]

class AddressAdmin(admin.ModelAdmin):
    list_display=('custom_id','unit_no','floor','building')
    



admin.site.register(Country,CountryAdmin)
admin.site.register(State,StateAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Locality,LocalityAdmin)

admin.site.register(LocalityType,LocalityTypeAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Plot,PlotAdmin)
admin.site.register(Building,BuildingAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Street,StreetAdmin)
admin.site.register(Landmark,LandmarkAdmin)
admin.site.register(DynamicRelationAreaLocality,DynamicRelationAreaLocalityAdmin)

