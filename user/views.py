from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserSerializer
from .models  import User

class CreateAdminUserViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class DetailAdminUserViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]