from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
