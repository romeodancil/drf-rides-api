from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils.timezone import now

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number=None, password=None, role='user'):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number=None, password=None):
        user = self.create_user(email, first_name, last_name, phone_number=None, password=None, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"

class RideModel(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)
    id_rider = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="rider"
    )
    id_driver = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="driver"
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(null=True, blank=True)

class RideEventModel(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        RideModel,
        on_delete=models.CASCADE,
        related_name="ride_event"
    )
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)