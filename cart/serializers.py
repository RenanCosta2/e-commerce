from rest_framework import serializers
from .models import Carts, ItensCart
from products.models import Products
from products.serializers import ProductsSerializer

class ItensCartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1)
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all()) 
    product_details = ProductsSerializer(source='product', read_only=True) 
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItensCart
        fields = [
            'id', 'product', 'cart', 'quantity', 'product_details', 'subtotal'
        ]
        read_only_fields = ['cart']

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.value
    
class CartsSerializers(serializers.ModelSerializer):
    items = ItensCartSerializer(many=True, read_only=True, source='itenscart_set')
    total = serializers.SerializerMethodField()
    data_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Carts
        fields = [
            'id', 'user', 'data_updated', 'items', 'total'
        ]
        read_only_fields = ['user']

    def get_total(self, obj):
        return sum(item.quantity * item.product.value for item in obj.itenscart_set.all())