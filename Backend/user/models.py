from email.policy import default
from django.db import models
from model_utils import Choices
from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email needs to be provided")
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                print("password is", password)
                user.set_password(password)
                user.save(using=self._db)
                return user

        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = Choices('customer', 'operator', 'manager')

    first_name = models.CharField("Name", max_length=240)
    last_name = models.CharField(null=True, blank=True, max_length=240)
    email = models.EmailField(null=True, blank=True, unique=True)
    user_type = models.CharField(
        choices=USER_TYPE, max_length=30, default=USER_TYPE.customer)
    # password

    created = models.DateField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # def save(self,*args,**kwargs):
    #    super(User,self).save(*args,**kwargs)
    #    return self

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(null=False, blank=False, max_length=250)
    address = models.CharField(max_length=300, null=False, blank=False)
    total_bikes = models.IntegerField(null=True, blank=True, default=0)


class Vehicle(models.Model):
    TYPE = Choices('electric_scooters', 'electric_bikes')

    type = models.CharField(choices=TYPE, max_length=30,
                            default=TYPE.electric_scooters)
    battery = models.IntegerField(null=True, blank=True, default=100)
    is_defective = models.BooleanField(null=True, blank=True, default=False)
    is_available = models.BooleanField(null=True, blank=True, default=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_bike', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=300, null=True, blank=True)


class Order(models.Model):
    start_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True, related_name='start_loc')
    end_location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True, related_name='end_loc')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(null=True, blank=True, default=True)


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(null=True, blank=True, default=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
