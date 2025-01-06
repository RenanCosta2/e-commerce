from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)

class Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Brazil')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city} - {self.zip_code}"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"