from django.db import models
from users.models import Users
from products.models import Products
from django.core.validators import MinValueValidator

class Carts(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    data_updated = models.DateTimeField(auto_now=True)

class ItensCart(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])