"""
Serializer for the Service Area model
"""
from rest_framework import serializers

from core.models import ServiceArea
from django.contrib.auth import get_user_model


class ProviderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Provider model
    """
    class Meta:
        model = get_user_model()
        fields = ('name',)


class ServiceAreaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service Area model
    """
    provider = ProviderSerializer(read_only=True)

    class Meta:
        """
        Meta class for the Service Area serializer
        """
        model = ServiceArea
        fields = ('id', 'name', 'price', 'provider', 'polygon')
        read_only_fields = ('provider',)
        write_only_fields = ('polygon',)
