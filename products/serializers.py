from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'category', 'description', 'value', 'storage', 'data_created', 'data_updated'
        ]

    