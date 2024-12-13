from rest_framework import serializers
from .models import Carts, ItensCart
from products.serializers import ProductsSerializer

class CartsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = [
            'id', 'user', 'data_updated'
        ]

class ItensCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItensCart
        fields = [
            'id', 'product', 'cart', 'quantity'
        ]
        read_only_fields = ['cart']