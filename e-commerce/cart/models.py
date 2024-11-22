from django.db import models
from users.models import Users
from products.models import Products

# Create your models here.
class Carts(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    data_updated = models.DateTimeField(auto_now=True)

class ItemCart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)