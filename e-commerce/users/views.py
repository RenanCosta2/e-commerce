from rest_framework import viewsets, status
from .serializers import UsersSerializer
from .models import Users
from cart.models import Carts
from rest_framework.response import Response

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                Carts.objects.create(user=user)
                return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Error registering user: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)