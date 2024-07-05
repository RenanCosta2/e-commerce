from django.shortcuts import render
from rest_framework import viewsets, response
from .serializers import PostSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticated

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)