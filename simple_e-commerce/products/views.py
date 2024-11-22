from rest_framework import viewsets, status
from .models import Products
from .serializers import ProductsSerializer
from rest_framework.response import Response
from .permissions import IsSuperUser
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            # permission_classes = [IsSuperUser]
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                product = serializer.save()
                return Response({'message': 'Product registered successfully!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Error registering product: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["GET"], url_path="filter_category")
    def browse_products_by_category(self, request):
        category = request.query_params.get('category')

        if not category:
            return Response({'detail': 'Category parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        products_by_category = Products.objects.filter(category=category)

        if not products_by_category.exists():
            return Response({'detail': f'No products found for category {category}'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(products_by_category, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path="filter_value")
    def browse_products_by_value(self, request):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if not min_price and not max_price:
            return Response({'detail': 'Min price and Max price parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not min_price:
            products_by_value = Products.objects.filter(value__lte=max_price)
        elif not max_price:
            products_by_value = Products.objects.filter(value__gte=min_price)
        else:
            if min_price > max_price:
                return Response({'detail': 'Min price parameter must be lower than Max price parameter.'}, status=status.HTTP_400_BAD_REQUEST)
            products_by_value = Products.objects.filter(value__range=(min_price, max_price))

        if not products_by_value.exists():
            return Response({'detail': 'No products found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(products_by_value, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path="filter_name")
    def browse_products_by_name(self, request):
        name = request.query_params.get('name')

        if not name:
            return Response({'detail': 'Name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        products_by_name = Products.objects.filter(name__icontains=name)

        if not products_by_name.exists():
            
            return Response({'detail': 'No products found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(products_by_name, many=True)
        return Response(serializer.data)
