from django.contrib import admin
from app_base.models import NewUser
# Register your models here.

class NewUserAdmin(admin.ModelAdmin):
    list_display=['id','username']

admin.site.register(NewUser,NewUserAdmin)

