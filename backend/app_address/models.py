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


class LocalityType(BaseModel,CustomIDMixin):
    locality_type_name=models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name='Locality Type'
        verbose_name_plural='Locality Type'
        

    def __str__(self):
        return f"{self.id}:{self.locality_type_name}"



class Locality(BaseModel,CustomIDMixin):
    
    locality_name=models.CharField( max_length=255, verbose_name='Locality Name')
    locality_type=models.ForeignKey(LocalityType, verbose_name='locality Type', on_delete=models.CASCADE, related_name='localities')
    pin_code=models.PositiveIntegerField(null=True,blank=True)
    city=models.ForeignKey(City, verbose_name="city", on_delete=models.CASCADE,related_name='localities')
    
    class Meta:
        verbose_name="Locality"
        verbose_name_plural="Localities"
        unique_together = ['locality_name', 'city']

    def __str__(self):
        pin_code_str = f" {self.pin_code}" if self.pin_code is not None else ""
        return f"{self.custom_id}:{self.locality_type}:{self.locality_name} {self.city} {pin_code_str}"


class SubLocality(BaseModel,CustomIDMixin):
    sub_locality_name=models.CharField( max_length=255, verbose_name='Sub Locality Name')
    locality=models.ForeignKey(Locality, verbose_name='locality', on_delete=models.CASCADE, related_name='sub_localities')
    
    class Meta:
        verbose_name='Sub Locality'
        verbose_name_plural='Sub Localities'
        unique_together=['sub_locality_name','locality']

    def __str__(self):
       return  f'{self.custom_id}:{self.sub_locality_name},{self.locality}'

class Area(BaseModel, CustomIDMixin):
    area_name = models.CharField(max_length=255,null=True,blank=True)
    localities = models.ManyToManyField(Locality, related_name='areas', null=True, blank=True)
    sub_localities = models.ManyToManyField(SubLocality, related_name='areas', null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL, related_name='areas')

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    def __str__(self):
        return f"{self.custom_id}:{self.area_name}"

    def clean(self):
        # Ensure that all localities and sub-localities have the same city
        cities_localities = set(locality.city for locality in self.localities.all())
        cities_sub_localities = set(sub_locality.locality.city for sub_locality in self.sub_localities.all())

        if len(cities_localities) == 1 and len(cities_sub_localities) == 1 and cities_localities==cities_sub_localities:
            # Set the unique city as the city attribute for the Area
            self.city = cities_localities.pop()
        else:
            raise ValidationError("All localities and sub-localities must belong to the same city within an Area.")

    


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
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='plots', null=True, blank=True)


    class Meta:
        verbose_name = "Plot"
        verbose_name_plural = "Plots"
        unique_together = ['plot_no', 'area','building']

    def __str__(self):
        return f"{self.custom_id}:{self.plot_no},{self.building},{self.area}"


# Create your models here.
class Address(BaseModel,CustomIDMixin):
    unit_no = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)

    building = models.ForeignKey(Building, verbose_name="addresses", on_delete=models.CASCADE,related_name='addresses', null=True,blank=True)
    plot_no = models.ManyToManyField(Plot, verbose_name="addresses",related_name='addresses',blank=True)
    
    # GenericForeignKey fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name="Address"
        verbose_name_plural="Address's"
        unique_together = ['unit_no', 'floor','building']

    def __str__(self):
        return f"{self.custom_id}:{self.unit_no}, {self.floor}, {self.building} ,{self.plot_no}"