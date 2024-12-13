from rest_framework import viewsets, status
from .models import Carts, ItensCart
from .serializers import CartsSerializers, ItensCartSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CartsViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartsSerializers

class ItensCartViewSet(viewsets.ModelViewSet):
    queryset = ItensCart.objects.all()
    serializer_class = ItensCartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                cart = Carts.objects.filter(user=self.request.user.id).first()
                item = serializer.save(cart=cart)
                return Response ({'message': 'Item added successfully.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Error adding the item: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
