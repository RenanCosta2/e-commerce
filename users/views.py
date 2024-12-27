from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import UsersSerializer
from .models import Users
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
