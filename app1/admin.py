from django.contrib import admin
from .models import UserModel,AmbulanceRequest
# Register your models here.

admin.site.register(UserModel)
admin.site.register(AmbulanceRequest)