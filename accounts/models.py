from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)