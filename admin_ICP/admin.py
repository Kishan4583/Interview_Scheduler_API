from django.contrib import admin

# import the model
from .models import User_Info, Interview_Info

# Register your models here.
admin.site.register(User_Info)
admin.site.register(Interview_Info)
