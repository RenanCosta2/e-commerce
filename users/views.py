from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from .serializers import UsersSerializer, AddressSerializer
from .models import Users, Address
from .permissions import IsAdminOrOwner
from cart.models import Carts

class UsersViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing `Users` in the system.

    Features:
        - CRUD operations on the `Users` model.
        - Automatically creates a cart for the user upon registration.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_permissions(self):
        """
        Override default permission logic.
        
        - The 'create' action is open to all users.
        - The 'list' action is restricted to admins.
        - Other actions (update, delete, get) are restricted to owners or admins.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]  # Open for all
        elif self.action == 'list':
            permission_classes = [IsAdminUser]  # Only admins can list users
        else:
            permission_classes = [IsAdminOrOwner, IsAuthenticated]  # Owners or admins for other actions
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new `User`.

        Validates the input data and saves the user to the database. Automatically creates
        a shopping cart (`Cart`) associated with the newly registered user. 

        Args:
            request: The HTTP request object containing user data.

        Returns:
            Response:
                - Success: A success message with a 201 status code when the user and cart are created successfully.
                - Error: A detailed error message with a 500 status code if there is a server error.
                - Validation Error: A 400 status code if the input data is invalid.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Save the user instance
                user = serializer.save()
                # Automatically create a cart for the newly registered user
                Carts.objects.create(user=user)
                return Response(
                    {'message': 'User registered successfully!'},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # Handle any server-side errors during user or cart creation
                return Response(
                    {'error': 'Error registering user: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        # Return validation errors if the input data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            address_default = Address.objects.filter(user=user, is_default=True).first()  # Get the current default address
            address_set_as_default = self.get_object()  # Get the address to be set as default

            # Check if there's a default address and update accordingly
            if address_default:
                address_default.is_default = False
                address_default.save()  # Set the current default address as non-default
            
            # Set the new address as the default
            address_set_as_default.is_default = True
            address_set_as_default.save()

            return Response({'message': 'Address set as default.'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors that occur during the update process
            return Response(
                {'error': 'An error occurred: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
