from django.db import models
from app_base.models import BaseModel
from app_base.mixins import CustomIDMixin
from app_address.models import Address

# Create your models here.
class PropertyFor(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)

class PropertyUse(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)
    
class PropertyType(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)

class Property(BaseModel,CustomIDMixin):
    area_in_sq_ft=models.PositiveIntegerField()
    property_for=models.ForeignKey(PropertyFor, verbose_name='property for', on_delete=models.CASCADE)
    property_use=models.ForeignKey(PropertyUse, verbose_name='property can be use', on_delete=models.CASCADE)
    property_type=models.ForeignKey(PropertyType, verbose_name='property type', on_delete=models.CASCADE)
    
class PropertyAddressRelationship(BaseModel,CustomIDMixin):
    address=models.ForeignKey(Address, verbose_name='address', on_delete=models.CASCADE,related_name='property_address_relationships')
    property=models.ForeignKey(Property, verbose_name='property', on_delete=models.CASCADE,related_name='property_address_relationships')