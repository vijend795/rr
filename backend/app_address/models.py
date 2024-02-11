from django.db import models

from app_base.models import BaseModel
from app_base.mixins import CustomIDMixin
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType



class Country(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255,verbose_name="country")
    code=models.CharField(max_length=50,verbose_name="country code")
    class Meta:
        verbose_name="Country"
        verbose_name_plural="Country"
    def __str__(self):
        return f"{self.custom_id}:{self.name} {self.code}"

class State(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255,verbose_name="State")
    country=models.ForeignKey(Country, verbose_name="country", on_delete=models.CASCADE,related_name='states')
    
    class Meta:
        verbose_name="State"
        verbose_name_plural="State"
        unique_together = [('name', 'country')]

    def __str__(self):
        return f"{self.custom_id}:{self.name} {self.country}"


class City(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255,verbose_name="City")
    state=models.ForeignKey(State, verbose_name="State", on_delete=models.CASCADE,related_name='cities')
    class Meta:
        verbose_name="City"
        verbose_name_plural="City"
        unique_together = [('name', 'state')]

    def __str__(self):
        return f"{self.custom_id}:{self.name} {self.state}"




class District(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=255)
    city=models.ForeignKey(City, verbose_name='city', on_delete=models.CASCADE,related_name='cities')
    def __str__(self):
        return f"{self.custom_id}:{self.name} "

class Tehsil(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=255)
    district=models.ForeignKey(District, verbose_name='district', on_delete=models.CASCADE, related_name='tehsils')
    def __str__(self):
        return f"{self.custom_id}:{self.name} "




# create locality dynamic with locality type like Sector , colony Vihar etc and can have sub Locality too for specific city 
class LocalityType(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name='Locality Type'
        verbose_name_plural='Locality Type'
    
    def save(self, *args, **kwargs):
        self.name = self.name.title()  # Capitalize the first letter
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.id}:{self.name}"

# Locality Includes sub locality and is sub locality exits then it will create a new locality 
class Locality(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=255, verbose_name='Locality Name')
    # sub_locality will handle block, sector part 1 -2 , etc 
    sub_locality_name=models.CharField( max_length=255, verbose_name='Sub Locality Name',null=True,blank=True)
    locality_type=models.ForeignKey(LocalityType, verbose_name='locality Type', on_delete=models.CASCADE, related_name='localities')
    city=models.ForeignKey(City, verbose_name="city", on_delete=models.CASCADE,related_name='localities')
    district=models.ForeignKey(District, verbose_name='district', on_delete=models.CASCADE, related_name='localities',null=True, blank=True)
    tehsil=models.ForeignKey(Tehsil, verbose_name='tehsil', on_delete=models.CASCADE, related_name='localities',null=True, blank=True)
    
    
    class Meta:
        verbose_name="Locality"
        verbose_name_plural="Localities"
        unique_together = [('locality_type','sub_locality_name','name', 'city')]

    def __str__(self):
     
        return f"{self.custom_id}:{self.locality_type}:{self.sub_locality_name}, {self.name}, {self.city}"


# area can have multiple unique locality adn create a area for address 



class Area(BaseModel,CustomIDMixin):
    pin_code=models.CharField( max_length=255,null=True, blank=True)

    class Meta:
        verbose_name='Area'
        verbose_name_plural='Area'
    def __str__(self):
        localities = AreaLocalityRelationship.objects.filter(area=self)
        locality_parts = []
        for relation in localities:
            locality_full_name = ""
            if relation.locality.sub_locality_name:
                locality_full_name += f"{relation.locality.sub_locality_name}-"
            locality_full_name += relation.locality.name
            locality_parts.append(locality_full_name)

        locality_names_str = ", ".join(locality_parts)
       
        city_name = localities.first().locality.city if localities else "Unknown City"
     
        return  f'{self.custom_id}:{locality_names_str}, {city_name},{self.pin_code} '

# now area can have multiple inline with locality and locality type   
class AreaLocalityRelationship(BaseModel,CustomIDMixin):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    # locality_type = models.ForeignKey(LocalityType, on_delete=models.CASCADE) # locality_type is part of Locality model
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE) 
    
class Street(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255)
    area=models.ForeignKey(Area, verbose_name='area', on_delete=models.CASCADE,related_name='streets')
    class Meta:
        unique_together = [('name', 'area')]
        
    def __str__(self):
        return f"{self.custom_id}:{self.name},{self.area}"

class Landmark(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255)
    area=models.ForeignKey(Area, verbose_name='area', on_delete=models.CASCADE,related_name='landmarks')
    class Meta:
        unique_together = [('name', 'area')]
        
    def __str__(self):
        return f"{self.custom_id}:{self.name},{self.area}"



    
class Plot(BaseModel, CustomIDMixin):
    plot_no = models.CharField(max_length=255)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='plots', null=True, blank=True)

    class Meta:
        verbose_name = "Plot"
        verbose_name_plural = "Plots"
        unique_together = [('plot_no', 'area')]

    def __str__(self):
        building = ", ".join([building.name for building in self.plot_building_relationships.all()])
        
        return f"{self.custom_id}:{self.plot_no},(Building : {building}),{self.area}"

class Building(BaseModel,CustomIDMixin):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name="Building"
        verbose_name_plural="Building's"

    def __str__(self):
        plots = ", ".join([plot.plot_no for plot in self.plot_building_relationships.all()])
       
        return f"{self.custom_id}:{self.name}, (Plots: {plots})"

class Tower(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255)
    block=models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        building = ", ".join([building.name for building in self.tower_building_relationships.all()])
       
        return f"{self.custom_id}:{self.name}, (Building: {building})"

class Floor(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)
    
    def __str__(self):
        tower = ", ".join([tower.name for tower in self.floor_tower_relationships.all()])
        plot = ", ".join([plot.name for plot in self.floor_tower_relationships.all()])
       
        return f"{self.custom_id}:{self.name}, (Tower: {tower}),(Plot: {plot})"

class Unit(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)
    
    def __str__(self):
        floor = ", ".join([floor.name for floor in self.unit_floor_relationships.all()])

        return f"{self.custom_id}:{self.name}, (Floor: {floor})"

class FloorPlotRelationship(BaseModel,CustomIDMixin):
    floor=models.ForeignKey(Floor, verbose_name='floor', on_delete=models.CASCADE,related_name='floor_plot_relationships')
    plot=models.ForeignKey(Plot, verbose_name='plot', on_delete=models.CASCADE,related_name='floor_plot_relationships')
    
class FloorTowerRelationship(BaseModel,CustomIDMixin):
    floor=models.ForeignKey(Floor, verbose_name='floor', on_delete=models.CASCADE,related_name='floor_tower_relationships')
    tower=models.ForeignKey(Tower, verbose_name='tower', on_delete=models.CASCADE,related_name='floor_tower_relationships')
    
class PlotBuildingRelationship(BaseModel,CustomIDMixin):
    plot=models.ForeignKey(Plot, verbose_name='plot', on_delete=models.CASCADE,related_name='plot_building_relationships')
    building=models.ForeignKey(Building, verbose_name='building', on_delete=models.CASCADE,related_name='plot_building_relationships')
    class Meta:
        unique_together = [('plot', 'building')]

class UnitFloorRelationship(BaseModel,CustomIDMixin):
    unit=models.ForeignKey(Unit, verbose_name='unit', on_delete=models.CASCADE,related_name='unit_floor_relationships')
    floor=models.ForeignKey(Floor, verbose_name='floor', on_delete=models.CASCADE,related_name='unit_floor_relationships')
    class Meta:
        unique_together = [('unit', 'floor')]
    
    
class TowerBuildingRelationship(BaseModel,CustomIDMixin):
    tower=models.ForeignKey(Tower, verbose_name='tower', on_delete=models.CASCADE,related_name='tower_building_relationships')
    building=models.ForeignKey(Building, verbose_name='building', on_delete=models.CASCADE,related_name='tower_building_relationships')
    class Meta:
        unique_together = [('tower', 'building')]

class StreetPlotRelationship(BaseModel, CustomIDMixin):
    street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='street_plot_relationships')
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='street_plot_relationships')
    class Meta:
        unique_together = [('plot', 'street')]
        
class StreetBuildingRelationship(BaseModel, CustomIDMixin):
    street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='street_building_relationships')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='street_building_relationships')
    class Meta:
        unique_together = [('building', 'street')]

class LandmarkPlotRelationship(BaseModel, CustomIDMixin):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='landmark_plot_relationships')
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='landmark_plot_relationships')
    
class LandmarkBuildingRelationship(BaseModel, CustomIDMixin):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='landmark_building_relationships')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='landmark_building_relationships')




# Create your models here.
class Address(BaseModel,CustomIDMixin):
    # address need to have either one of the value to link with property
    unit_no = models.ForeignKey(Unit, verbose_name="unit", on_delete=models.CASCADE,related_name='addresses', null=True,blank=True)
    floor = models.ForeignKey(Floor, verbose_name="floor", on_delete=models.CASCADE,related_name='addresses', null=True,blank=True)
    building = models.ForeignKey(Building, verbose_name="building", on_delete=models.CASCADE,related_name='addresses', null=True,blank=True)
    plot = models.ForeignKey(Plot, verbose_name="plot", on_delete=models.CASCADE,related_name='addresses', null=True,blank=True)


    class Meta:
        verbose_name="Address"
        verbose_name_plural="Address's"
        # unique_together = [('unit_no', 'floor','building','plot')]


    def __str__(self):
        return f"{self.custom_id}:{self.unit_no}{self.floor}{self.building}{self.plot}"

    def clean(self):
        super().clean()
        fields = [self.unit_no, self.floor, self.building, self.plot]
        populated_fields = [field for field in fields if field]
        if len(populated_fields) != 1:
            raise ValidationError("Address must have exactly one of the following: unit_no, floor, building, plot")