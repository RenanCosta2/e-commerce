from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Products
from products.serializers import ProductsSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())
    product_details = ProductsSerializer(source='product', read_only=True)
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'product_details', 'value', 'quantity', 'item_total'
        ]
        read_only_fields = ['order']

    def get_item_total(self, obj):
        return obj.quantity * obj.value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'address', 'items', 'total_value', 'status'
        ]
        read_only_fields = ['user', 'items', 'total_value']
