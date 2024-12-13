from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'username', 'first_name', 'last_name', 'cpf', 'email', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user