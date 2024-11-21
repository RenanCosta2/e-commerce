from rest_framework import viewsets, status
from .models import Products
from .serializers import ProductsSerializer
from rest_framework.response import Response
from .permissions import IsSuperUser
from rest_framework.permissions import AllowAny

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
