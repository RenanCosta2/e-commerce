from django.db import models
from users.models import Users
from products.models import Products
from django.core.validators import MinValueValidator

class Carts(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    data_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.user.first_name} Cart"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

class ItensCart(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.cart.user.email} - Item cart: {self.product.name}"

    class Meta:
        verbose_name = "Item Cart"
        verbose_name_plural = "Items Cart"