from django.db import models
from Auth.models import MyUser


class Category(models.Model):
    """
    Creates categories for our food products.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Creates products objects for each food collected and inserted in
    our database.
    """
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    nutri_grade = models.CharField(max_length=10)
    url = models.URLField()
    stores = models.CharField(max_length=200)
    ingredients = models.TextField()
    image_small = models.URLField()
    image_xl = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    users = models.ManyToManyField(MyUser, related_name='favorites')
    code = models.CharField(max_length=50, null=True)
    date = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_better_food(self, product):
        """
        Method required to look for better food in the database.
        It is based on the category of the product given by the
         user of the website.
        """
        category = product.category
        result = Product.objects.filter(category=category)
        return result.order_by('nutri_grade')
