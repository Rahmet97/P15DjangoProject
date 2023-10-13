from django.contrib import admin
from .models import Service, Image, ShoppingCart

admin.site.register((Service, Image, ShoppingCart))
