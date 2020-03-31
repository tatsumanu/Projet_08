from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Products(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    nutri_grade = models.CharField(max_length=10)
    ingredients = models.TextField()
    store = models.CharField(max_length=200)
    url = models.URLField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
