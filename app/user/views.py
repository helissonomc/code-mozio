"""
Views for the user API.
"""
from rest_framework import generics

from django.contrib.auth import get_user_model

from user.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    Endpoint to create user.
    """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
