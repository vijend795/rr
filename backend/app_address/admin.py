from django.contrib import admin,messages
from django.db import IntegrityError
from django.utils.translation import ngettext
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db import models


# Register your models here.


from app_address.models import Address,City,State,Country,Locality,Plot,Building,LocalityType, Area, AreaLocalityRelationship,Street,Landmark,StreetPlotRelationship, LandmarkPlotRelationship,Unit,Floor,Tower,PlotBuildingRelationship,FloorPlotRelationship,UnitFloorRelationship,FloorTowerRelationship,TowerBuildingRelationship,StreetBuildingRelationship,LandmarkBuildingRelationship

# Inline 

class PlotBuildingRelationshipInline(admin.TabularInline):
    model=PlotBuildingRelationship
    extra=1
    
class FloorPlotRelationshipInline(admin.TabularInline):
    model=FloorPlotRelationship
    extra=1
    
class UnitFloorRelationshipInline(admin.TabularInline):
    model=UnitFloorRelationship
    extra=1
class FloorTowerRelationshipInline(admin.TabularInline):
    model=FloorTowerRelationship
    extra=1
class TowerBuildingRelationshipInline(admin.TabularInline):
    model=TowerBuildingRelationship
    extra=1
class StreetBuildingRelationshipInline(admin.TabularInline):
    model=StreetBuildingRelationship
    extra=1
class LandmarkBuildingRelationshipInline(admin.TabularInline):
    model=LandmarkBuildingRelationship
    extra=1
    
    
    
class PlotInline(admin.TabularInline):
    model=Plot
    extra=1

class BuildingInline(admin.TabularInline):
    model=Building
    extra=1
    
class TowerInline(admin.TabularInline):
    model=Tower
    extra=1

class LocalityInline(admin.TabularInline):
    model=Locality
    extra=1

class AreaLocalityRelationshipInline(admin.TabularInline):
    model = AreaLocalityRelationship
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
    model=Country
    list_display=('custom_id','name','code',)
    inlines=[StateInline]

class StateAdmin(admin.ModelAdmin):
    model=State
    list_display=('custom_id','name','country',)
    inlines=[CityInline]

class CityAdmin(admin.ModelAdmin):
    model=City
    list_display=('custom_id','name','state')
    inlines=[LocalityInline]

class LocalityTypeAdmin(admin.ModelAdmin):
    model=LocalityType
    list_display=('custom_id','name')
    actions = ['duplicate_selected']


   



class LocalityAdmin(admin.ModelAdmin):
    model=Locality
    list_display=('custom_id','locality_type','sub_locality_name','name', 'tehsil','district','city')


class AreaAdmin(admin.ModelAdmin):
    model=AreaLocalityRelationship
    list_display=('custom_id','pin_code','display_localities')
    inlines=[AreaLocalityRelationshipInline,PlotInline]

    def display_localities(self, obj):
        localities = AreaLocalityRelationship.objects.filter(area=obj).order_by('-locality')
        if localities:
            return mark_safe("<br>".join(f"{relation.locality.locality_type} - {relation.locality}" for relation in localities))
        return ""
    display_localities.short_description = "Localities"
    
class StreetAdmin(admin.ModelAdmin):
    list_display=('custom_id','name','get_plot_numbers')   
    inlines=[StreetPlotRelationshipInline]
    
    def get_plot_numbers(self, obj):
        plot_numbers = obj.street_plot_relationships.all().order_by('plot__plot_no')
        # return ", ".join(str(relationship.plot.plot_no) for relationship in plot_numbers)
        if plot_numbers:
            return mark_safe("<br>".join(str(relationship.plot.plot_no) for relationship in plot_numbers))
        return ""


    get_plot_numbers.short_description = 'Plot Numbers'

class LandmarkAdmin(admin.ModelAdmin):
    list_display=('custom_id','name','get_plot_numbers')  
    inlines=[LandmarkPlotRelationshipInline] 
    def get_plot_numbers(self, obj):
        plot_numbers = obj.landmark_plot_relationships.all().order_by('plot__plot_no')
        # return ", ".join(str(relationship.plot.plot_no) for relationship in plot_numbers)
        if plot_numbers:
            return mark_safe("<br>".join(str(relationship.plot.plot_no) for relationship in plot_numbers))
        return ""

    get_plot_numbers.short_description = 'Plot Numbers'



class PlotAdmin(admin.ModelAdmin):
    list_display=('custom_id','plot_no','area','get_all_streets','get_all_landmark')
    inlines=[StreetPlotRelationshipInline,LandmarkPlotRelationshipInline]

    def get_all_streets(self, obj):
        street_relationships = obj.street_plot_relationships.all().order_by('-street__name')
        # return ", ".join(f"{relationship.street.street_name} (Order: {relationship.order})" for relationship in street_relationships)
        if street_relationships:
            return mark_safe("<br>".join(str(relationship.street.name)for relationship in street_relationships))
        return ""

    def get_all_landmark(self, obj):
        landmark_relationships = obj.landmark_plot_relationships.all().order_by('-landmark__name')
        # return ", ".join(f"{relationship.landmark.landmark_name} (Order: {relationship.order})" for relationship in landmark_relationships)
        if landmark_relationships:
            return mark_safe("<br>".join(str(relationship.landmark.name)for relationship in landmark_relationships))
        return ""

    get_all_streets.short_description="Streets"
    get_all_landmark.short_description="Landmark"



class BuildingAdmin(admin.ModelAdmin):
    model=Building
    list_display=('custom_id','name')
    inlines=[PlotBuildingRelationshipInline,TowerBuildingRelationshipInline]
    
class TowerAdmin(admin.ModelAdmin):
    model=Tower
    list_display=('custom_id','name')
    inlines=[TowerBuildingRelationshipInline,FloorTowerRelationshipInline]
   
class UnitAdmin(admin.ModelAdmin):
    model=Unit
    list_display=('custom_id','name')
    inlines=[UnitFloorRelationshipInline]
   
class FloorAdmin(admin.ModelAdmin):
    model=Floor
    list_display=('custom_id','name')
    inlines=[FloorTowerRelationshipInline,FloorPlotRelationshipInline,UnitFloorRelationshipInline]


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
admin.site.register(Floor,FloorAdmin)
admin.site.register(Tower,TowerAdmin)

