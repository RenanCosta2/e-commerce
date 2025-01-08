from django.db import models
from products.models import Products
from users.models import Users, Address
from django.core.validators import MinValueValidator
from decimal import Decimal

class Order(models.Model):
    STATUS = [
        ("AWAITING_PAYMENT", "Awaiting payment"),
        ("PAYMENT_APPROVED", "Payment approved"),
        ("IN_PREPARATION", "In preparation"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_value = models.DecimalField(
    max_digits=15,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.0'))] 
    )
    status = models.CharField(choices=STATUS, default="AWAITING_PAYMENT", max_length=17)

    def __str__(self):
        return f"Order#{self.id} - {self.user.first_name}, {self.total_value}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    value = models.DecimalField(
    max_digits=15,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.0'))] 
    )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])