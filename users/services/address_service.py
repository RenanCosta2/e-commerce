from ..models import Address

class AddressService:
    """
    A service class for handling business logic related to user addresses.
    """

    @staticmethod
    def set_as_default(user, address):
        """
        Sets a specific address as the default for the given user.

        - Updates the current default address (if it exists) to non-default.
        - Marks the specified address as the new default.

        Args:
            user: The user who owns the addresses.
            address: The address to set as default.
        """
        current_default = Address.objects.filter(user=user, is_default=True).first()  # Get the current default address

        # If there's a default address, mark it as non-default
        if current_default:
            current_default.is_default = False
            current_default.save()
        
        # Set the new address as the default
        address.is_default = True
        address.save()
