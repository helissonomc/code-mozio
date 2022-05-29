"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)


class UserCreateView(generics.CreateAPIView):
    """
    Endpoint to create user.
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Endpoint to create a new auth token.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer
