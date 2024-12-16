from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import Products
from .serializers import ProductsSerializer
from .permissions import IsSuperUser

class ProductsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing `Products` in the system.

    Features:
        - CRUD operations on `Products` model.
        - Custom filtering actions to browse products by category, price range, and name.
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def get_permissions(self):
        """
        Returns the appropriate permissions based on the current action.

        - `list` and `retrieve`: Allow any user to access these endpoints.
        - Other actions: Require the user to have `IsSuperUser` permissions.
        """
        if self.action not in ['list', 'retrieve']:
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new `Product`.

        Validates the input data and saves the product to the database. If there
        is an error during the save process, a detailed error message is returned.

        Args:
            request: The HTTP request object containing the product data.

        Returns:
            Response: A success message with a 201 status code if the product is 
            created successfully, otherwise a detailed error response.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'message': 'Product registered successfully.'},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': 'Error registering product: ' + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], url_path="filter_category")
    def browse_products_by_category(self, request):
        """
        Filters products by category.

        Query Parameters:
            - `category` (str): The category to filter products by (required).

        Returns:
            Response: A list of products matching the category or a 404 error
            if no products are found.
        """
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'detail': 'Category parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        products_by_category = Products.objects.filter(category=category)
        if not products_by_category.exists():
            return Response(
                {'detail': f'No products found for category {category}'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(products_by_category, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="filter_value")
    def browse_products_by_value(self, request):
        """
        Filters products by a price range.

        Query Parameters:
            - `min_price` (float): The minimum price (optional).
            - `max_price` (float): The maximum price (optional).

        Returns:
            Response: A list of products matching the price range or a 404 error
            if no products are found. A 400 error is returned if parameters are missing
            or invalid.
        """
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if not min_price and not max_price:
            return Response(
                {'detail': 'Min price and Max price parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not min_price:
            products_by_value = Products.objects.filter(value__lte=max_price)
        elif not max_price:
            products_by_value = Products.objects.filter(value__gte=min_price)
        else:
            if float(min_price) > float(max_price):
                return Response(
                    {'detail': 'Min price parameter must be lower than Max price parameter.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            products_by_value = Products.objects.filter(
                value__range=(min_price, max_price)
            )

        if not products_by_value.exists():
            return Response(
                {'detail': 'No products found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(products_by_value, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path="filter_name")
    def browse_products_by_name(self, request):
        """
        Filters products by name (case insensitive).

        Query Parameters:
            - `name` (str): The partial or full name of the product to search for (required).

        Returns:
            Response: A list of products matching the name or a 404 error
            if no products are found.
        """
        name = request.query_params.get('name')
        if not name:
            return Response(
                {'detail': 'Name parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        products_by_name = Products.objects.filter(name__icontains=name)
        if not products_by_name.exists():
            return Response(
                {'detail': 'No products found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(products_by_name, many=True)
        return Response(serializer.data)
