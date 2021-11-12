from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Users(AbstractUser):

    is_verified = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    contact_number = models.BigIntegerField(default=0)
    otp = models.IntegerField(default=0)

