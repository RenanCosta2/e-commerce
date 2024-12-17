from rest_framework import viewsets, status
from .models import Products
from .serializers import ProductsSerializer
from rest_framework.response import Response
from .permissions import IsSuperUser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

# ViewSet to manage product-related CRUD operations
class ProductsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations and custom actions for Products.

    This ViewSet provides:
    - Default CRUD operations (list, create, retrieve, update, delete).
    - Custom actions for filtering products by category, value, and name.
    - Permission logic to restrict certain actions to superusers only.
    """
    queryset = Products.objects.all()  # Queryset to retrieve all products
    serializer_class = ProductsSerializer  # Serializer to handle product data

    def get_permissions(self):
        """
        Override default permission logic.

        - 'list' and 'retrieve' actions are open to all users.
        - Other actions (create, update, delete) are restricted to superusers.
        """
        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsSuperUser]  # Custom permission for superusers
        else:
            permission_classes = [AllowAny]  # Open access for public endpoints
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Custom create method to register a new product.

        - Validates input data using the serializer.
        - Saves the product if valid and handles any errors.
        - Returns a success response with status 201 or an error response.
        """
        serializer = self.get_serializer(data=request.data)  # Deserialize and validate input data
        if serializer.is_valid():
            try:
                product = serializer.save()  # Save the product instance
                return Response(
                    {'message': 'Product registered successfully.'},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # Handle unexpected errors during product save
                return Response(
                    {'error': 'Error registering product: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        # Return a 400 response if input data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], url_path="filter_category")
    def browse_products_by_category(self, request):
        """
        Custom action to filter products by category.

        Query Parameters:
            - category: The category to filter products by.

        Returns:
            - List of products in the given category or appropriate error messages.
        """
        category = request.query_params.get('category')  # Get category parameter

        if not category:
            return Response(
                {'detail': 'Category parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve products matching the given category
        products_by_category = Products.objects.filter(category=category)

        if not products_by_category.exists():
            return Response(
                {'detail': f'No products found for category {category}'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the matching products
        serializer = self.get_serializer(products_by_category, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="filter_value")
    def browse_products_by_value(self, request):
        """
        Custom action to filter products by price range.

        Query Parameters:
            - min_price: Minimum product price (optional).
            - max_price: Maximum product price (optional).

        Returns:
            - List of products within the given price range or appropriate error messages.
        """
        # Retrieve query parameters for price filtering
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        # Validate input parameters
        if not min_price and not max_price:
            return Response(
                {'detail': 'Min price and Max price parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter products based on price range
        if not min_price:
            products_by_value = Products.objects.filter(value__lte=max_price)
        elif not max_price:
            products_by_value = Products.objects.filter(value__gte=min_price)
        else:
            # Ensure min_price is less than max_price
            if float(min_price) > float(max_price):
                return Response(
                    {'detail': 'Min price parameter must be lower than Max price parameter.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            products_by_value = Products.objects.filter(value__range=(min_price, max_price))

        # Handle case where no products are found
        if not products_by_value.exists():
            return Response(
                {'detail': 'No products found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the matching products
        serializer = self.get_serializer(products_by_value, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path="filter_name")
    def browse_products_by_name(self, request):
        """
        Custom action to filter products by name.

        Query Parameters:
            - name: The name (or partial name) to search products by.

        Returns:
            - List of products matching the given name or appropriate error messages.
        """
        name = request.query_params.get('name')  # Get name parameter

        if not name:
            return Response(
                {'detail': 'Name parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter products where name contains the given value (case insensitive)
        products_by_name = Products.objects.filter(name__icontains=name)

        if not products_by_name.exists():
            return Response(
                {'detail': 'No products found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the matching products
        serializer = self.get_serializer(products_by_name, many=True)
        return Response(serializer.data)
