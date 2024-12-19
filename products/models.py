from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Products(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    value = models.DecimalField(
    max_digits=15,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.0'))] 
    )
    storage = models.IntegerField(validators=[MinValueValidator(0)])
    data_created = models.DateTimeField(auto_now_add=True)
    data_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.category} - {self.name}: {self.value}'