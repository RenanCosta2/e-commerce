from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Carts, ItensCart
from .serializers import ItensCartSerializer

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

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return ItensCart.objects.all()
        
        return ItensCart.objects.filter(cart__user=user)

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle adding items to the authenticated user's cart.

        Functionality:
        - Validates the incoming data using the serializer.
        - Checks if the product already exists in the user's cart:
            - If it exists, increments the quantity of the product.
            - If it doesn't exist, adds a new item to the cart.
        - Ensures proper error handling and returns appropriate responses.

        Steps:
        - Deserialize and validate the incoming data using the serializer.
        - Retrieve the authenticated user's cart.
        - Check if the product already exists in the cart:
            - If it exists, update the quantity and save the changes.
            - If not, create a new item associated with the user's cart.
        - Return a success response if the operation succeeds.
        - Handle unexpected errors and return appropriate error messages.

        Args:
            request: The HTTP request containing item data to be added to the cart.

        Returns:
            Response: A JSON response with a success or error message.
                - HTTP 201 (Created): If the item is successfully added or updated in the cart.
                - HTTP 400 (Bad Request): If the serializer validation fails.
                - HTTP 500 (Internal Server Error): If an unexpected error occurs during the operation.
        """
        # Deserialize and validate the incoming data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Retrieve the cart associated with the authenticated user
                cart = Carts.objects.filter(user=self.request.user.id).first()

                # Check if the product already exists in the user's cart
                product = serializer.validated_data['product']
                product_in_cart = ItensCart.objects.filter(cart=cart, product=product).first()

                if product_in_cart:
                    # Increment the quantity if the product already exists in the cart
                    product_in_cart.quantity += serializer.validated_data['quantity']
                    product_in_cart.save()
                    return Response({'message': 'Item added successfully.'}, status=status.HTTP_201_CREATED)

                # Save the new item in the user's cart
                item = serializer.save(cart=cart)

                return Response({'message': 'Item added successfully.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Handle unexpected errors during the save process
                return Response(
                    {'error': 'Error adding the item: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Return a 400 Bad Request response if the serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def reduce_quantity(self, request, pk=None):
        """
        Custom PATCH method to reduce the quantity of an item in the cart.

        Functionality:
        - Decreases the quantity of an item in the authenticated user's cart by 1.
        - If the item's quantity becomes 1 and is reduced further, the item is removed from the cart.
        - Ensures proper error handling and returns appropriate responses.

        Steps:
        - Retrieve the cart item using the provided primary key (`pk`).
        - Check if the quantity is greater than 1:
            - If yes, reduce the quantity by 1 and save the changes.
            - If the quantity is 1, delete the item from the cart.
        - Handle unexpected errors and return appropriate error messages.

        Args:
            request: The HTTP request (not directly used but required by DRF).
            pk: The primary key of the cart item to be modified.

        Returns:
            Response: A JSON response with a success or error message.
                - HTTP 200 (OK): If the item quantity is successfully reduced.
                - HTTP 204 (No Content): If the item is successfully removed from the cart.
                - HTTP 400 (Bad Request): If the item's quantity cannot be reduced further.
                - HTTP 500 (Internal Server Error): If an unexpected error occurs during the operation.
        """
        try:
            # Retrieve the cart item by primary key
            item = self.get_object()

            if item.quantity > 1:
                # Reduce quantity and save changes
                item.quantity -= 1
                item.save()
                return Response({'message': 'Item quantity reduced successfully.'}, status=status.HTTP_200_OK)
            elif item.quantity == 1:
                # Delete the item if quantity reaches 1
                item.delete()
                return Response({'message': 'Item removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Prevent reducing below 1
                return Response({'error': 'Quantity cannot be reduced below 1.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {'error': 'An error occurred: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
