from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..serializers import AddressSerializer
from ..models import Address
from ..services.address_service import AddressService

class AddressViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing user addresses.

    Features:
        - Allows users to manage their addresses (CRUD operations).
        - Restricts access to authenticated users.
        - Automatically sets the first address as the default if no default address exists.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users only
    service = AddressService

    def get_queryset(self):
        """
        Customizes the queryset based on the user's authentication status.

        - For admin users (staff), returns all addresses.
        - For regular users, filters addresses to only show the ones belonging to them.

        Returns:
            queryset: The list of addresses based on user permissions.
        """
        user = self.request.user

        if user.is_staff:
            return Address.objects.all()  # Admins can view all addresses
        
        return Address.objects.filter(user=user)  # Regular users can only view their own addresses
    
    def perform_create(self, serializer):
        """
        Customizes the creation of a new address.

        - If the user already has an address, the new address will be created without being marked as default.
        - If the user does not have any addresses, the new address will be created as the default address.

        Args:
            serializer: The validated serializer containing the address data.
        """
        user = self.request.user
        user_address = Address.objects.filter(user=user).exists()  # Check if the user already has an address

        if user_address:
            serializer.save(user=user)  # Create a non-default address if the user has addresses
        else:
            serializer.save(user=user, is_default=True)  # Create the first address as the default one

    @action(detail=True, methods=['patch'])
    def set_as_default(self, request, pk=None):
        """
        Action to set a specific address as the default for the authenticated user.

        - This action updates the default address for the user by setting the previously default address as non-default
          and marking the selected address as the new default.
        
        Args:
            request: The HTTP request object containing address data.
            pk: The primary key of the address to be set as default.

        Returns:
            Response: A response indicating the success or failure of the operation.
        """
        try:
            user = self.request.user
            address_to_set = self.get_object()  # Get the address to be set as default

            self.service.set_as_default(user, address_to_set)

            return Response({'message': 'Address set as default.'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors that occur during the update process
            return Response(
                {'error': 'An error occurred: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
