from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
import random
import uuid
# Create your models here.

# AbstractUser
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    objects = UserManager()

    GENERAL = 0
    ADMIN = 1
    ROLE_CHOICES = (
        (GENERAL, 'General'),
        (ADMIN, 'Admin'),
    )
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=200, blank=True, default="")
    last_name = models.CharField(_('last name'), max_length=200, blank=True, default="")
    telefon = models.CharField(max_length=100,blank=True, default="")
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=0)
    cocoBikeChain = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name","last_name","password"]

    def __str__(self):
        n = ""
        r = ""
        res = ""
        try:
            n = self.email
        except:
            pass
        try:
            r = self.ROLE_CHOICES[self.role][1]
        except:
            pass
        return f'{n} | {r}'

class Bike(models.Model):
    secret = models.UUIDField(
         primary_key = False,
         unique=True,
         default = uuid.uuid4,
         editable = True)
    code = models.UUIDField(
         primary_key = False,
         unique=True,
         default = uuid.uuid4,
         editable = True)

class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name="reservations")
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, null=False, blank=False, related_name="reservations")
    active = models.BooleanField(default=False)

class BikeData(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, null=True, blank=True,related_name="data")
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name="data")
    lat=models.CharField(max_length=256,default="")
    lon=models.CharField(max_length=256,default="")
    battery=models.FloatField(default=0)
