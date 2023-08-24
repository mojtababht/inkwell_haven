from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
from .validators import PhoneNumberValidator

class User(AbstractUser):

    phone_no_validator = PhoneNumberValidator
    username = None
    email=None
    phone_no =models.CharField(
        max_length=150,
        unique=True,
        validators=[phone_no_validator],
        error_messages={
            "unique": "A user with that phone number already exists.",
        },

    )
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name +' ' +self.last_name






