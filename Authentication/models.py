from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','phone_number']
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # class Meta:
    #     ordering = ['-created_at']

    @property
    def jwt_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.token),
        }


