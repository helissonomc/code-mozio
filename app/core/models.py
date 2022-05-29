from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom user manager to deal with emails instead of usernames
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Provider(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ServiceArea(models.Model):
    """
    Service area model
    """

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Geojson information
    description = models.CharField(max_length=255)
    polygon = models.PolygonField(srid=4326)

    def __str__(self):
        return self.name
