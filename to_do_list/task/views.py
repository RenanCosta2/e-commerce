from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import TaskSerializer, CategorySerializer, UserSerializer
from .models import Task, Category
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from .permissions import IsOwner

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False ,methods=["GET"])
    def completed(self, request):
        completed_tasks = self.get_queryset().filter(status=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False ,methods=["GET"])
    def pending(self, request):
        pending_tasks = self.get_queryset().filter(status=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False ,methods=["GET"])
    def select_category(self, request):
        category_id = request.query_params.get('category', None)

        if category_id is not None:
            task_category = self.get_queryset().filter(category=category_id)
            serializer = self.get_serializer(task_category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Category parameter not provided.'}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'list']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'list' and self.request.user.is_staff:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()