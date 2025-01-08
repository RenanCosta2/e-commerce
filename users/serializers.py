from rest_framework import serializers
from .models import Users, Address

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'username', 'first_name', 'last_name', 'cpf', 'email', 'password'
        ]
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'user', 'street', 'city', 'state', 'zip_code', 'country', 'is_default'
        ]
        read_only_fields = ['user']