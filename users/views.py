from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import UsersSerializer
from .models import Users
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
