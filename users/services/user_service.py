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
        user = Users.objects.create(**data)
        # Create a cart associated with the user
        Carts.objects.create(user=user)
        return user
