from django.contrib import admin
from .models import Category, Product


# Registering the Product and Category models
admin.site.register(Category)
admin.site.register(Product)
