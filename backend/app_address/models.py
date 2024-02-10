from django.db import models

from app_base.models import BaseModel
from app_base.mixins import CustomIDMixin
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType



class Country(BaseModel,CustomIDMixin):
    country_name=models.CharField(max_length=255)
    country_mobile_code=models.CharField(max_length=50)
    class Meta:
        verbose_name="Country"
        verbose_name_plural="Countries"
    def __str__(self):
        return f"{self.custom_id}:{self.country_name} {self.country_mobile_code}"

class State(BaseModel,CustomIDMixin):
    state_name=models.CharField(max_length=255)
    country=models.ForeignKey(Country, verbose_name="state", on_delete=models.CASCADE,related_name='states')
    
    class Meta:
        verbose_name="State"
        verbose_name_plural="State's"
        unique_together = ['state_name', 'country']

    def __str__(self):
        return f"{self.custom_id}:{self.state_name} {self.country}"


class City(BaseModel,CustomIDMixin):
    city_name=models.CharField(max_length=255)
    state=models.ForeignKey(State, verbose_name="city", on_delete=models.CASCADE,related_name='cities')
    class Meta:
        verbose_name="City"
        verbose_name_plural="Cities"
        unique_together = ['city_name', 'state']

    def __str__(self):
        return f"{self.custom_id}:{self.city_name} {self.state}"




class District(BaseModel,CustomIDMixin):
    district=models.CharField( max_length=255)
    city=models.ForeignKey(City, verbose_name='city', on_delete=models.CASCADE,related_name='cities')

class Tehsil(BaseModel,CustomIDMixin):
    teshil=models.CharField( max_length=255)
    district=models.ForeignKey(District, verbose_name='district', on_delete=models.CASCADE, related_name='tehsils')




# create locality dynamic with locality type like Sector , colony Vihar etc and can have sub Locality too for specific city 
class LocalityType(BaseModel,CustomIDMixin):
    locality_type_name=models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name='Locality Type'
        verbose_name_plural='Locality Type'
    def __str__(self):
        return f"{self.id}:{self.locality_type_name}"

# Locality Includes sub locality and is sub locality exits then it will create a new locality 
class Locality(BaseModel,CustomIDMixin):
    locality_name=models.CharField( max_length=255, verbose_name='Locality Name')
    sub_locality_name=models.CharField( max_length=255, verbose_name='Sub Locality Name',null=True,blank=True)
    locality_type=models.ForeignKey(LocalityType, verbose_name='locality Type', on_delete=models.CASCADE, related_name='localities')
    city=models.ForeignKey(City, verbose_name="city", on_delete=models.CASCADE,related_name='localities')
    
    
    class Meta:
        verbose_name="Locality"
        verbose_name_plural="Localities"
        unique_together = ['locality_type','sub_locality_name','locality_name', 'city']

    def __str__(self):
     
        return f"{self.custom_id}:{self.locality_type}:{self.sub_locality_name}, {self.locality_name}, {self.city}"


# area can have multiple unique locality adn create a area for address 

# now area can have multiple inline with locality and locality type   
class DynamicRelationAreaLocality(BaseModel,CustomIDMixin):
    area = models.ForeignKey('app_address.Area', on_delete=models.CASCADE)
    locality_type = models.ForeignKey(LocalityType, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE) 

class Area(BaseModel,CustomIDMixin):
    pin_code=models.CharField( max_length=255,null=True, blank=True)

    class Meta:
        verbose_name='Area'
        verbose_name_plural='Area'
    def __str__(self):
        localities = DynamicRelationAreaLocality.objects.filter(area=self)
        locality_parts = []
        for relation in localities:
            locality_full_name = ""
            if relation.locality.sub_locality_name:
                locality_full_name += f"{relation.locality.sub_locality_name}-"
            locality_full_name += relation.locality.locality_name
            locality_parts.append(locality_full_name)

        locality_names_str = ", ".join(locality_parts)
       
        city_name = localities.first().locality.city if localities else "Unknown City"
     
        return  f'{self.custom_id}:{locality_names_str}, {city_name},{self.pin_code} '


class Street(BaseModel,CustomIDMixin):
    street_name=models.CharField(max_length=255)
    area=models.ForeignKey(Area, verbose_name='area', on_delete=models.CASCADE,related_name='streets')
    def __str__(self):
        return f"{self.custom_id}:{self.street_name},{self.area}"

class Landmark(BaseModel,CustomIDMixin):
    landmark_name=models.CharField(max_length=255)
    area=models.ForeignKey(Area, verbose_name='area', on_delete=models.CASCADE,related_name='landmarks')
    def __str__(self):
        return f"{self.custom_id}:{self.landmark_name},{self.area}"


class Building(BaseModel,CustomIDMixin):
    building_name = models.CharField(max_length=255)
    tower_no=models.CharField(max_length=255,null=True,blank=True)
    block=models.CharField(max_length=255,null=True,blank=True)


    class Meta:
        verbose_name="Building"
        verbose_name_plural="Building's"

    def __str__(self):
        return f"{self.custom_id}:{self.building_name}"
    
class Plot(BaseModel, CustomIDMixin):
    plot_no = models.CharField(max_length=255)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='plots', null=True, blank=True)


    class Meta:
        verbose_name = "Plot"
        verbose_name_plural = "Plots"
        unique_together = ['plot_no', 'area']

    def __str__(self):
        return f"{self.custom_id}:{self.plot_no},{self.building},{self.area}"

class StreetPlotRelationship(BaseModel, CustomIDMixin):
    street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name='street_plot_relationships')
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='street_plot_relationships')

class LandmarkPlotRelationship(BaseModel, CustomIDMixin):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='landmark_plot_relationships')
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='landmark_plot_relationships')




# Create your models here.
class Address(BaseModel,CustomIDMixin):
    unit_no = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)

    building = models.ForeignKey(Building, verbose_name="addresses", on_delete=models.CASCADE,related_name='addresses', null=True,blank=True)
    plot_no = models.ManyToManyField(Plot, verbose_name="addresses",related_name='addresses',blank=True)



    class Meta:
        verbose_name="Address"
        verbose_name_plural="Address's"
        unique_together = ['unit_no', 'floor','building']

    def __str__(self):
        return f"{self.custom_id}:{self.unit_no}, {self.floor}, {self.building} ,{self.plot_no}"