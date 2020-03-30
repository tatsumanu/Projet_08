from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=200)
    ingredients = models.TextField()
