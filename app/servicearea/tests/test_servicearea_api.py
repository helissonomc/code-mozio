"""
Test Service Area API
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Polygon, Point

from rest_framework import status
from rest_framework.test import APIClient

from core.models import ServiceArea

from servicearea.serializers import ServiceAreaSerializer

from decimal import Decimal


SERVICEAREA_URL = reverse('servicearea:servicearea-list')


def detail_url(servicearea_id):
    """
    Return the detail URL for a service area
    """
    return reverse('servicearea:servicearea-detail', args=[servicearea_id])


def create_servicearea(provider, **params):
    """
    Create a service area
    """
    return ServiceArea.objects.create(provider=provider, **params)


def create_user(**params):
    """
    Create a user
    """
    return get_user_model().objects.create_user(**params)


class PublicServiceAreaApiTests(TestCase):
    """
    Test the publicly available service area API
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required for retrieving service areas
        """
        res = self.client.get(SERVICEAREA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateServiceAreaApiTests(TestCase):
    """
    Test the authorized user service area API
    """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@test.com',
            password='Testpass123',
            name='Test Name',
            phone_number='+123456789',
            language='en',
            currency='USD'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_service_areas(self):
        """
        Test retrieving service areas
        """
        create_servicearea(
            self.user, name='Test Service Area 1',
            polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            price=Decimal('1.00'),
            description='Test Service 1'
        )
        create_servicearea(
            self.user, name='Test Service Area 2',
            polygon=Polygon(((0, 0), (0, 2), (2, 2), (2, 0), (0, 0))),
            price=Decimal('2.00'),
            description='Test Service 2'
        )

        lat_lng = Point(0.5, 1.5)
        res = self.client.get(
            SERVICEAREA_URL,
            {'latitude': lat_lng.y, 'longitude': lat_lng.x}
        )

        service_areas = ServiceArea.objects.filter(polygon__contains=lat_lng).all()
        serializer = ServiceAreaSerializer(service_areas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_service_area_successful(self):
        """
        Test creating a new service area
        """
        payload = {
            'name': 'Test Service Area',
            'polygon': [
                {'lat': 0, 'lng': 0},
                {'lat': 0, 'lng': 1},
                {'lat': 1, 'lng': 1},
                {'lat': 1, 'lng': 0},
                {'lat': 0, 'lng': 0},
            ],
            'price': Decimal('1.00'),
            'description': 'Test Service'
        }

        res = self.client.post(SERVICEAREA_URL, payload)

        self.assertEqual(res.data.get('provider').get('name'), self.user.name)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_service_area(self):
        """
        Test updating a service area
        """
        service_area = create_servicearea(
            self.user, name='Test Service Area',
            polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            price=Decimal('1.00'),
            description='Test Service'
        )

        payload = {
            'name': 'Updated Service Area',
            'price': Decimal('2.00'),
            'polygon': [
                {'lat': -2, 'lng': 0},
                {'lat': 0, 'lng': 1},
                {'lat': 1, 'lng': 1},
                {'lat': 1, 'lng': 0},
                {'lat': 0, 'lng': 0},
            ],
        }

        res = self.client.patch(detail_url(service_area.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        service_area.refresh_from_db()
        self.assertEqual(service_area.name, payload.get('name'))
        self.assertEqual(service_area.price, payload.get('price'))

    def test_update_other_provider(self):
        """
        Test updating other user's service area
        """
        user2 = create_user(
            email='test2@test.com',
            password='Testpass123',
            name='Test2 Name',
            phone_number='+1223456789',
            language='en',
            currency='USD'
        )
        service_area = create_servicearea(
            user2, name='Test Service Area',
            polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            price=Decimal('1.00'),
            description='Test Service'
        )

        payload = {
            'name': 'Updated Service Area',
            'price': Decimal('2.00')
        }

        res = self.client.patch(detail_url(service_area.id), payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_service_area(self):
        """
        Test deleting a service area
        """
        service_area = create_servicearea(
            self.user, name='Test Service Area',
            polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            price=Decimal('1.00'),
            description='Test Service'
        )

        res = self.client.delete(detail_url(service_area.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceArea.objects.count(), 0)
