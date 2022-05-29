"""
Views for the service area APIs
"""
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException

import json

from django.contrib.gis.geos import Point, Polygon

from servicearea.serializers import ServiceAreaSerializer

from core.models import ServiceArea


class ServiceAreaViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint that allows service areas to be viewed or edited.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filter the queryset based on the user
        """

        longitude = float(self.request.query_params.get('longitude'))
        latitude = float(self.request.query_params.get('latitude'))
        point = Point(longitude, latitude)

        return ServiceArea.objects.filter(polygon__contains=point)

    def perform_create(self, serializer):
        """
        Create a new service area
        """

        try:
            polygon = self.request.data.getlist('polygon')
            polygon = [json.loads(i.replace("'", "\"")) for i in polygon]
        except Exception:
            polygon = self.request.data['polygon']

        try:
            polygon = Polygon([(float(i['lat']), float(i['lng'])) for i in polygon])
        except Exception:
            raise APIException("Polygon is not valid")


        serializer.save(provider=self.request.user, polygon=polygon)


class ServiceAreaUpdateViewSet(mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    API endpoint that allows service areas to be edited.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filter the queryset based on the user
        """
        return ServiceArea.objects.filter(provider=self.request.user)

    def perform_update(self, serializer):
        """
        Create a new service area
        """

        try:
            polygon = self.request.data.getlist('polygon')
            polygon = [json.loads(i.replace("'", "\"")) for i in polygon]
        except Exception:
            polygon = self.request.data['polygon']

        try:
            polygon = Polygon([(float(i['lat']), float(i['lng'])) for i in polygon])
        except Exception:
            raise APIException("Polygon is not valid")

        serializer.save(provider=self.request.user, polygon=polygon)
