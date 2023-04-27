"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for User"""
    def create_user(self, email, password = None, **extra_fields):
        """Create & return a new user"""
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


# model for User table
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    # avatar = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # add more fields here

    objects = UserManager()

    USERNAME_FIELD = 'email'




#model for Category table
class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=255)
    # add more fields here

    def __str__(self):
        return self.category_name

#model for Tag table
class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tag_name = models.CharField(max_length=255)
    # add more fields here

    def __str__(self):
        return self.tag_name

#model for Discount table
class Discount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    discount_title = models.CharField(max_length=255)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    # add more fields here

    def __str__(self):
        return self.discount_title


class TagConnector(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)+' - '+str(self.category)

class CategoryConnector(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)+' - '+str(self.category)


class DiscountConnector(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)+' - '+str(self.discount)


#model for Product table
class Product(models.Model):
    product_title = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_color = models.CharField(max_length=24)
    product_detail = models.TextField()

    def __str__(self):
        return str(self.product_title)