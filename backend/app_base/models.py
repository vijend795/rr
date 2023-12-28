from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings
import pytz
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


class BaseModel(models.Model):
    # id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    temp_id=models.CharField(max_length=255,null=True, blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='%(class)s_created',null=True,blank=True)
    updated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='%(class)s_updated',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='Created At')
    updated_at=models.DateTimeField(auto_now=True,verbose_name='Updated At')
    active_status=models.BooleanField(default=True)

    class Meta:
        abstract=True
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # This is a new instance, set the created_by field
            self.created_by = kwargs.pop('created_by', None)
            self.created_at=kwargs.pop('created_at',None)
          
        # Always set the updated_by and updated_at fields
        self.updated_at = timezone.now()
        # Get the logged-in user, if available
        user = kwargs.pop('updated_by', None)

        if user and isinstance(user, get_user_model()):
            # Set the updated_by field only if a valid user is provided
            self.updated_by = user
        

        super().save(*args, **kwargs)

class NewUser(AbstractUser):
    Gender_Choice=[
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),  
    ]  
    temp_id=models.CharField(max_length=255,blank=True,null=True)
    gender=models.CharField(max_length=100,choices=Gender_Choice,null=True,blank=True)
    phone = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999999999)],  # Adjust the maximum value as needed
        null=True,
        blank=True
    )
    dob=models.DateField(default=None, blank=True, null=True)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    nationality=models.CharField(max_length=255,null=True,blank=True)
    # to avoid circular reference 
    # address=models.ForeignKey("app_address.Address", verbose_name="Address", on_delete=models.PROTECT,null=True,blank=True)
    
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"