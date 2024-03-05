from django.db import models
from app_base.models import BaseModel
from app_base.mixins import CustomIDMixin
from app_address.models import Unit,Floor,Tower,Building,Plot
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


# Create your models here.
class PropertyFor(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)

class PropertyUse(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)
    
class PropertyType(BaseModel,CustomIDMixin):
    name=models.CharField( max_length=50)

# class Property(BaseModel,CustomIDMixin):
#     area_in_sq_ft=models.PositiveIntegerField()
#     property_for=models.ForeignKey(PropertyFor, verbose_name='property for', on_delete=models.CASCADE)
#     property_use=models.ForeignKey(PropertyUse, verbose_name='property can be use', on_delete=models.CASCADE)
#     property_type=models.ForeignKey(PropertyType, verbose_name='property type', on_delete=models.CASCADE)
    

class Property(BaseModel,CustomIDMixin):

    unit=models.ForeignKey(Unit, verbose_name='unit', on_delete=models.PROTECT,null=True, blank=True)
    floor=models.ForeignKey(Floor, verbose_name='floor', on_delete=models.PROTECT,null=True, blank=True)
    tower=models.ForeignKey(Tower, verbose_name='tower', on_delete=models.PROTECT,null=True, blank=True)
    building=models.ForeignKey(Building, verbose_name='building', on_delete=models.PROTECT,null=True, blank=True)
    plot=models.ForeignKey(Plot, verbose_name='plot', on_delete=models.PROTECT,null=True, blank=True)
    
    def clean(self):
        super().clean()
        fields = [self.unit, self.floor, self.tower, self.building, self.plot]
        filled_fields = [field for field in fields if field]
        if len(filled_fields) != 1:
            raise ValidationError('Exactly one of unit, floor, tower, building, or plot should be set.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.custom_id}"

class SubPropertyType(BaseModel,CustomIDMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubProperty(BaseModel, CustomIDMixin):
    sub_property_type = models.ForeignKey(SubPropertyType, on_delete=models.CASCADE, related_name='sub_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='sub_properties')
    # Add other fields specific to sub-properties like floors, units, towers
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='unit_sub_properties')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, blank=True, related_name='floor_sub_properties')
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE, null=True, blank=True, related_name='tower_sub_properties')

    
    def clean(self):
        super().clean()
        if self.sub_property_type.name == "Unit" and not self.unit:
            raise ValidationError("Unit must be specified for sub_property_type 'Unit'.")
        if self.sub_property_type.name == "Floor" and not self.floor:
            raise ValidationError("Floor must be specified for sub_property_type 'Floor'.")
        if self.sub_property_type.name == "Tower" and not self.tower:
            raise ValidationError("Floor must be specified for sub_property_type 'Floor'.")


    def __str__(self):
        return f"{self.custom_id}"

    







# # Signal receiver function to create SubPropertyType instances after migrations
# @receiver(post_migrate)
# def create_sub_property_types(sender, **kwargs):
#     if sender.name == 'app_property':
#         # Check if SubPropertyType instances already exist
#         if not SubPropertyType.objects.exists():
#             # Create SubPropertyType instances for unit, floor, and tower
#             SubPropertyType.objects.create(name="Unit")
#             SubPropertyType.objects.create(name="Floor")
#             SubPropertyType.objects.create(name="Tower")