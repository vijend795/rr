from django.db import models

from app_base.models import BaseModel
from app_base.mixins import CustomIDMixin
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver



class Country(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255,verbose_name="country")
    code=models.CharField(max_length=50,verbose_name="country code")
    class Meta:
        verbose_name="Country"
        verbose_name_plural="Country"
    def __str__(self):
        # return f"{self.custom_id}:{self.name} {self.code}"
        return f"{self.name} "

class State(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255,verbose_name="State")
    country=models.ForeignKey(Country, verbose_name="country", on_delete=models.CASCADE,related_name='states')
    
    class Meta:
        verbose_name="State"
        verbose_name_plural="State"
        unique_together = [('name', 'country')]

    def __str__(self):
        # return f"{self.custom_id}:{self.name} {self.country}"
        return f"{self.name}, {self.country}"


class City(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255,verbose_name="City")
    state=models.ForeignKey(State, verbose_name="State", on_delete=models.CASCADE,related_name='cities')
    class Meta:
        verbose_name="City"
        verbose_name_plural="City"
        unique_together = [('name', 'state')]

    def __str__(self):
        # return f"{self.custom_id}:{self.name} {self.state}"
        # return f"{self.name}, {self.state}"
        return f"{self.name}"




class District(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=255)
    city=models.ForeignKey(City, verbose_name='city', on_delete=models.CASCADE,related_name='districts')
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
    locality_type=models.ForeignKey(LocalityType, verbose_name='locality Type', on_delete=models.CASCADE, related_name='localities',null=True,blank=True)
    city=models.ForeignKey(City, verbose_name="city", on_delete=models.CASCADE,related_name='localities')
    district=models.ForeignKey(District, verbose_name='district', on_delete=models.CASCADE, related_name='localities',null=True, blank=True)
    tehsil=models.ForeignKey(Tehsil, verbose_name='tehsil', on_delete=models.CASCADE, related_name='localities',null=True, blank=True)
    
    
    class Meta:
        verbose_name="Locality"
        verbose_name_plural="Localities"
        unique_together = [('locality_type','sub_locality_name','name', 'city')]

    def __str__(self):
        if self.sub_locality_name:
            
            # return f"{self.custom_id}:{self.locality_type}:{self.sub_locality_name}, {self.name}, {self.city}"
            return f"{self.sub_locality_name}, {self.name}, {self.city}"
        else:
            # return f"{self.custom_id}:{self.locality_type}:{self.name}, {self.city}"
            return f"{self.name}, {self.city}"


# area can have multiple unique locality adn create a area for address 


class Block(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=50)
    # link Block with colony only in later stage to fill data 
    locality=models.ForeignKey(Locality, verbose_name='locality', on_delete=models.CASCADE)
    remark=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.custom_id}: {self.name}, {self.locality}"
    
class Area(BaseModel,CustomIDMixin):
    pin_code = models.CharField(max_length=255, null=True, blank=True)
    localities = models.ManyToManyField('Locality', through='AreaLocality', verbose_name='localities')
    block=models.ForeignKey(Block, verbose_name='block', on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        verbose_name='Area'
        verbose_name_plural='Area'
        
    def get_locality_id_set(self):
        id_set=set()
        for locality in self.area_locality_relations.all():
            id_set.add(locality.locality.custom_id)
        
        return id_set


    def __str__(self):
        
        # locality_info = ", ".join([f"{area_loc.locality.locality_type}: {area_loc.locality.sub_locality_name}, {area_loc.locality.name}, {area_loc.locality.city.name}, {area_loc.locality.city.state.name}" for area_loc in self.area_locality_relations.all()])
        locality_id= ", ".join([f"{area_loc.locality.custom_id}" for area_loc in self.area_locality_relations.all()])
        # return f"Area ID: {self.custom_id},  Localities: {locality_info}, Pin Code: {self.pin_code}, ID:{locality_id}"
        # locality_info = ", ".join([f" {area_loc.locality.sub_locality_name}, {area_loc.locality.name}" for area_loc in self.area_locality_relations.all()])
        city=set()
        city_name=None
        for area_loc in self.area_locality_relations.all():
            # print("city:",area_loc.locality)
            city.add(area_loc.locality.city)
            city_name=area_loc.locality.city
        
        if len(city)>1:
            print("error finding city from locality , multiple city name exits for area :{self.custom_id} ")
            
        locality_info = ", ".join([f"{area_loc.locality.sub_locality_name}, {area_loc.locality.name}" 
                           if area_loc.locality.sub_locality_name is not None 
                           else f"{area_loc.locality.name}" 
                           for area_loc in self.area_locality_relations.all()])
        if self.pin_code:
            
            return f"{locality_info}, {city_name}, {self.pin_code}"
        else:
            return f"{locality_info}, {city_name}"
        


class AreaLocality(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE,related_name='area_locality_relations')
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE,related_name='area_locality_relations')

    class Meta:
        unique_together = ('area', 'locality')
    
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
    area=models.ForeignKey(Area, verbose_name='area', on_delete=models.CASCADE, related_name='plot')

    class Meta:
        verbose_name = "Plot"
        verbose_name_plural = "Plots"
        unique_together = [('plot_no', 'area')]
        

    def __str__(self):
        return f"{self.custom_id}:{self.plot_no}"

# class PlotAreaRelationships(BaseModel,CustomIDMixin):
#     plot=models.ForeignKey(Plot, verbose_name='plot', on_delete=models.CASCADE, related_name='plot_area_relationships')
    
#     landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='plot_area_relationships')
#     street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='plot_area_relationships')
    
#     class Meta:
#         verbose_name = "Plot and area"
#         verbose_name_plural = "Plot and Area "
#         unique_together = [('plot', 'area')]


class Building(BaseModel,CustomIDMixin):
    name = models.CharField(max_length=255)
    area=models.ForeignKey(Area, verbose_name='area', on_delete=models.CASCADE, related_name='building')

    class Meta:
        verbose_name="Building"
        verbose_name_plural="Building's"
        unique_together = [('name', 'area')]

    def __str__(self):
        plots = ", ".join([obj.plot.plot_no for obj in self.plot_building_relationships.all()])
        if plots:
            # return f"{self.custom_id}:{self.name}, (Plots: {plots})"
            return f"{self.name}, {plots}"
        else:
            return f"{self.name}"

class Tower(BaseModel,CustomIDMixin):
    name=models.CharField(max_length=255)
    block=models.CharField(max_length=255,null=True,blank=True, default=None)
    class Meta:
        verbose_name="Tower"
        verbose_name_plural="Tower"
        unique_together = [('name', 'block')]
    
    # def validate_unique(self, exclude=None):
    #     super().validate_unique(exclude)

    #     if self.block is None:
    #         # If block is None, check if a Tower with the same name exists
    #         towers_with_same_name = Tower.objects.filter(name=self.name, block__isnull=True)
    #         if towers_with_same_name.exists() and self.pk != towers_with_same_name.first().pk:
    #             raise ValidationError({'name': 'A Tower with this name already exists.'})
    #     else:
    #         # If block is not None, check if a Tower with the same name and block exists
    #         towers_with_same_name_and_block = Tower.objects.filter(name=self.name, block=self.block)
    #         if towers_with_same_name_and_block.exists() and self.pk != towers_with_same_name_and_block.first().pk:
    #             raise ValidationError({'block': 'A Tower with this name and block already exists.'})
            
    
    def __str__(self):
        building = ", ".join([obj.building.name for obj in self.tower_building_relationships.all()])
       
        return f"{self.custom_id}:{self.name}, (Building: {building})"

class Floor(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50, unique=True)
    
    def __str__(self):
        tower = ", ".join([obj.tower.name for obj in self.floor_tower_relationships.all()])
        plot = ", ".join([obj.plot.plot_no for obj in self.floor_plot_relationships.all()])
       
        return f"{self.custom_id}:{self.name}, (Tower: {tower}),(Plot: {plot})"

class Unit(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50,unique=True)
    
    def __str__(self):
        floor = ", ".join([obj.floor.name for obj in self.unit_floor_relationships.all()])

        return f"{self.custom_id}:{self.name}, (Floor: {floor})"

class FloorPlotRelationship(BaseModel,CustomIDMixin):
    floor=models.ForeignKey(Floor, verbose_name='floor', on_delete=models.CASCADE,related_name='floor_plot_relationships')
    plot=models.ForeignKey(Plot, verbose_name='plot', on_delete=models.CASCADE,related_name='floor_plot_relationships')
    class Meta:
        unique_together = [('plot', 'floor')]
        
class FloorTowerRelationship(BaseModel,CustomIDMixin):
    floor=models.ForeignKey(Floor, verbose_name='floor', on_delete=models.CASCADE,related_name='floor_tower_relationships')
    tower=models.ForeignKey(Tower, verbose_name='tower', on_delete=models.CASCADE,related_name='floor_tower_relationships')
    class Meta:
        unique_together = [('floor', 'tower')]
        
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
    class Meta:
        unique_together = [('plot', 'landmark')]
        
class LandmarkBuildingRelationship(BaseModel, CustomIDMixin):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='landmark_building_relationships')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='landmark_building_relationships')
    class Meta:
        unique_together = [('building', 'landmark')]


