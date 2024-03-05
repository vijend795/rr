from django.contrib import admin,messages
from django.db import IntegrityError
from django.utils.translation import ngettext
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db import models


# Register your models here.


from app_address.models import City,State,Country,Locality,Plot,Building,LocalityType, Area,AreaLocality, Street,Landmark,StreetPlotRelationship, LandmarkPlotRelationship,Unit,Floor,Tower,PlotBuildingRelationship,FloorPlotRelationship,UnitFloorRelationship,FloorTowerRelationship,TowerBuildingRelationship,StreetBuildingRelationship,LandmarkBuildingRelationship,Block

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
    
class AreaLocalityInline(admin.TabularInline):
    model = AreaLocality
    extra = 1 
    
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
    

class AreaLocalityAdmin(admin.ModelAdmin):
    model=AreaLocality
    list_display=('custom_id','area','localities')
    
class BlockAdmin(admin.ModelAdmin):
    model=Block
    list_display=('custom_id','name','locality')
    
class AreaAdmin(admin.ModelAdmin):
    model=Area
    list_display=('custom_id','block','display_localities','pin_code')
    inlines=[AreaLocalityInline,PlotInline]

    def display_localities(self, obj):
        localities = obj.localities.all()
        
        if localities:
            # return mark_safe("<br>".join(f"{locality.locality_type} - {locality.name}" for locality in localities))
            return mark_safe("<br>".join(f"{locality}" for locality in localities))
        return ""
    
    display_localities.short_description = "Localities"
    
class StreetAdmin(admin.ModelAdmin):
    list_display=('custom_id','name','get_plot_numbers','get_buildings','area')   
    inlines=[StreetPlotRelationshipInline,StreetBuildingRelationshipInline]
    
    def get_plot_numbers(self, obj):
        plot_numbers = obj.street_plot_relationships.all().order_by('plot__plot_no')
        # return ", ".join(str(relationship.plot.plot_no) for relationship in plot_numbers)
        if plot_numbers:
            return mark_safe("<br>".join(str(relationship.plot.plot_no) for relationship in plot_numbers))
        return ""
    def get_buildings(self,obj):
        buildings=obj.street_building_relationships.all()
        
        if buildings:
            return mark_safe("<br>".join(str(relationship.building.name) for relationship in buildings))

        return ""

    get_plot_numbers.short_description = 'Plot Numbers'
    get_buildings.short_description = 'Buildings '

class LandmarkAdmin(admin.ModelAdmin):
    list_display=('custom_id','name','get_plot_numbers','get_buildings',"area")  
    inlines=[LandmarkPlotRelationshipInline,LandmarkBuildingRelationshipInline] 
    def get_plot_numbers(self, obj):
        plot_numbers = obj.landmark_plot_relationships.all().order_by('plot__plot_no')
        # return ", ".join(str(relationship.plot.plot_no) for relationship in plot_numbers)
        if plot_numbers:
            return mark_safe("<br>".join(str(relationship.plot.plot_no) for relationship in plot_numbers))
        return ""
    
    def get_buildings(self,obj):
        buildings=obj.landmark_building_relationships.all()
        
        if buildings:
            return mark_safe("<br>".join(str(relationship.building.name) for relationship in buildings))

        return ""

    get_plot_numbers.short_description = 'Plot Numbers'
    get_buildings.short_description = 'Buildings'



class PlotAdmin(admin.ModelAdmin):
    list_display=('custom_id','plot_no','area','get_all_streets','get_all_landmark')
    inlines=[StreetPlotRelationshipInline,LandmarkPlotRelationshipInline]
    list_filter=('area__localities__city__state','area',)
    search_fields = ['custom_id', 'plot_no', 'area__localities__name', 'area__localities__sub_locality_name']


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
    list_display=('custom_id','name','get_all_towers','get_all_plots','get_all_floor','area')
    inlines=[PlotBuildingRelationshipInline,TowerBuildingRelationshipInline,StreetBuildingRelationshipInline,LandmarkBuildingRelationshipInline]
    
    def get_all_towers(self,obj):
        towers=obj.tower_building_relationships.all()
        if towers:
            return mark_safe("<br>".join(str(relationship.tower.name)for relationship in towers))
        else:
            return ""
        
    def get_all_plots(self,obj):
        plots=obj.plot_building_relationships.all()
        if plots:
            return mark_safe("<br>".join(str(relationship.plot.plot_no)for relationship in plots))
        else:
            return ""
        
    def get_all_floor(self,obj):
        towers = obj.tower_building_relationships.all()
        floors_set = set()  # Initialize an empty set to store unique floors
        
        for tower in towers:
            floors = tower.tower.floor_tower_relationships.all()
            all_floor = f"<br>Tower: {tower.tower.name} <br>"  # Initialize all_floor with tower info
            
            if floors:
                all_floor += "<br>".join(f"{floor.floor.name}  " for floor in floors)
                # all_floor += "<br>".join(f"{floor.floor.name} ({floor.tower.name})<br>{'<br>'.join(relation.building.name for relation in floor.tower.tower_building_relationships.all() if obj.name == relation.building.name)}" for floor in floors)

                floors_set.add(all_floor)
            else:
                floors_set.add("No floors")  # If no floors, add a message to indicate that
            
        if floors_set:
            return mark_safe("<br>".join(floors_set))
        else:
            return ""
       
    
    get_all_plots.short_description="Plot"
    get_all_towers.short_description="Tower"
    get_all_floor.short_description="Floor"
    
class TowerAdmin(admin.ModelAdmin):
    model=Tower
    list_display=('custom_id','name','block','get_all_buildings','get_all_floor')
    inlines=[TowerBuildingRelationshipInline,FloorTowerRelationshipInline]
    list_filter=('tower_building_relationships__building','name',)
    
    def get_all_buildings(self,obj):
        buildings=obj.tower_building_relationships.all()
        if buildings:
            return mark_safe("<br>".join((str(relationship.building.name) for relationship in buildings)))
        return ""
    
    def get_all_floor(self,obj):
        floors=obj.floor_tower_relationships.all()
        if floors:
            return mark_safe("<br>".join((str(relationship.floor.name) for relationship in floors)))
        return ""
   
    
    get_all_buildings.short_description="Buildings"
    get_all_floor.short_descriptions="Floors"
    
    
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
admin.site.register(Block,BlockAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Plot,PlotAdmin)
admin.site.register(Building,BuildingAdmin)

admin.site.register(Street,StreetAdmin)
admin.site.register(Landmark,LandmarkAdmin)
admin.site.register(Floor,FloorAdmin)
admin.site.register(Tower,TowerAdmin)

