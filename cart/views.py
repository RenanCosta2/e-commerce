from rest_framework import viewsets, status
from .models import Carts, ItensCart
from .serializers import CartsSerializers, ItensCartSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# ViewSet for managing Carts
class CartsViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Carts.

    Provides default implementations for listing, retrieving, creating, 
    updating, and deleting cart instances.
    """
    queryset = Carts.objects.all()  # Queryset to fetch all Cart objects
    serializer_class = CartsSerializers  # Serializer to handle Cart data

# ViewSet for managing items in the cart
class ItensCartViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for items in the cart.

    Ensures that only authenticated users can perform operations, and provides 
    custom behavior for adding items to a user's cart.
    """
    queryset = ItensCart.objects.all()  # Queryset to fetch all ItemCart objects
    serializer_class = ItensCartSerializer  # Serializer to handle ItemCart data
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users only

    def create(self, request, *args, **kwargs):
        """
        Custom create method to add items to the authenticated user's cart.

        Steps:
        - Validates the incoming data using the serializer.
        - Retrieves the cart associated with the authenticated user.
        - Saves the item to the user's cart and returns a success response.
        - Handles errors during the save process and returns appropriate error messages.

        Args:
            request: The HTTP request containing item data.

        Returns:
            Response: A success or error response based on the operation.
        """
        # Deserialize and validate the incoming data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Retrieve the cart associated with the authenticated user
                cart = Carts.objects.filter(user=self.request.user.id).first()

                # Save the new item in the user's cart
                item = serializer.save(cart=cart)

                # Return a success response
                return Response({'message': 'Item added successfully.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Handle any unexpected errors during the save process
                return Response(
                    {'error': 'Error adding the item: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Return a 400 Bad Request response if the serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
