from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'username', 'first_name', 'last_name', 'cpf', 'email', 'password'
        ]

    def create(self, validated_data):
        """
        Custom `create` method to securely handle user password.

        Args:
            validated_data (dict): Validated user data.

        Returns:
            Users: The created user instance with an encrypted password.
        """
        password = validated_data.pop('password')  # Extract password from input
        user = Users(**validated_data)  # Create user instance with remaining data
        user.set_password(password)  # Encrypt the password
        user.save()  # Save the user to the database
        return user  # Return the created user