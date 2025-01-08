from users.models import Users
from cart.models import Carts

class UserService:
    """
    Service class for user-related business logic.
    """
    
    @staticmethod
    def create_user(data):
        """
        Create a new user and associate a shopping cart.

        Args:
            data (dict): User data to create the `Users` instance.

        Returns:
            Users: The newly created user instance.
        """
        # Create the user instance
        password = data.pop('password')
        user = Users(**data)
        user.set_password(password)
        user.save()

        # Create a cart associated with the user
        Carts.objects.create(user=user)
        return user
