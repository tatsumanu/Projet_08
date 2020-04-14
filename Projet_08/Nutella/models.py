from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError("L'identifiant doit être une adresse mail!")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='adresse mail',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100, verbose_name='pseudo')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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
