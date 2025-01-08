from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Carts, ItensCart
from users.models import Address
from django.db import transaction

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for orders.

    Ensures that only authenticated users can perform operations, with special 
    permissions for admins. Custom behavior is included to handle cart 
    processing, address validation, and order creation.
    """
    queryset = Order.objects.all()  # Queryset to fetch all Order objects
    serializer_class = OrderSerializer  # Serializer to handle Order data
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users only

    def get_queryset(self):
        """
        Custom method to retrieve orders based on the user's role.

        If the user is a staff member, they can view all orders. Otherwise, only 
        orders associated with the authenticated user are returned.

        Args:
            None

        Returns:
            Queryset: Orders related to the authenticated user or all orders for staff.
        """
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        return Order.objects.filter(user=user)

    def get_permissions(self):
        """
        Custom permission method to dynamically assign permissions based on the action.

        The `list`, `retrieve`, and `create` actions require authentication, while 
        other actions require admin access.

        Args:
            None

        Returns:
            list: List of permission classes for the current action.
        """
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle order creation based on the user's cart and address.

        Functionality:
        - Validates the existence of the user's cart and address.
        - Calculates the total order value based on the cart items.
        - Creates a new order and order items while updating product stock.
        - Deletes the cart items after order creation.

        Steps:
        - Validates that the cart is not empty and retrieves the address.
        - Creates an order instance with the provided address and total value.
        - Creates order items and updates the stock for each product.
        - Deletes items from the cart once the order is successfully created.
        - Handles errors gracefully and returns appropriate error messages.

        Args:
            request: The HTTP request containing user data for order creation.

        Returns:
            Response: A JSON response with a success or error message.
                - HTTP 201 (Created): If the order is successfully processed.
                - HTTP 400 (Bad Request): If the cart is empty or the address is invalid.
                - HTTP 500 (Internal Server Error): If an unexpected error occurs.
        """
        try:
            # Retrieve the user's cart
            cart = Carts.objects.filter(user=request.user).first()
            if not cart:
                return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve cart items
            cart_items = ItensCart.objects.filter(cart=cart)
            
            # Retrieve the user's address
            address = Address.objects.filter(id=request.data.get("address"), user=request.user).first()
            if not address:
                return Response({'error': "Address not found or not exists."}, status=status.HTTP_404_NOT_FOUND)

            # Calculate total order value based on cart items
            total_value = sum(item.product.value * item.quantity for item in cart_items)

            with transaction.atomic():
                # Create the order instance
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_value=total_value
                )

                # Create order items and update product stock
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        value=item.product.value,
                        quantity=item.quantity,
                    )

                    # Update product stock
                    product = item.product
                    product.storage -= item.quantity
                    product.save()

                # Delete cart items after order creation
                cart_items.delete()

                # Serialize and return the order data
                serializer = self.get_serializer(order)
            
            return Response({'message': 'Order processed.', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle errors during order creation
            return Response(
                {"error": f"Error creating the order: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
