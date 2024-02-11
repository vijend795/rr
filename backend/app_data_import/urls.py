from django.contrib import admin
from django.urls import path

from app_data_import.views import Upload_property_data,UploadStatus

urlpatterns = [
    path('property_data/', Upload_property_data , name='upload-property-data'),
    path('upload_status/', UploadStatus.as_view() , name='upload-status'),
]