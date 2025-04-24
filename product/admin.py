from django.contrib import admin
from . import models
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Cart_added)
admin.site.register(models.OrderPlaced)
admin.site.register(models.Address)
# admin.site.register(User)