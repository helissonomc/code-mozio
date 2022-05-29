"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Polygon, Point

from core.models import ServiceArea


class ModelTests(TestCase):
    """
    Test for models
    """
    def setUp(self) -> None:
        self.user_test = {
            'email': 'test@test.com',
            'password': 'Testpass123',
            'name': 'Test Name',
            'phone_number': '+123456789',
            'language': 'en',
            'currency': 'USD',
        }

        self.sample_email = {
            ('test1@EXAMPLE.com', 'test1@example.com'),
            ('test2@EXAMPLE.com', 'test2@example.com'),
        }
        return super().setUp()

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """
        user = get_user_model().objects.create_user(
            email=self.user_test['email'],
            password=self.user_test['password'],
            name=self.user_test['name'],
            phone_number=self.user_test['phone_number'],
            language=self.user_test['language'],
            currency=self.user_test['currency']
        )

        self.assertEqual(user.email, self.user_test['email'])
        self.assertEqual(user.name, self.user_test['name'])
        self.assertEqual(user.phone_number, self.user_test['phone_number'])
        self.assertEqual(user.language, self.user_test['language'])
        self.assertEqual(user.currency, self.user_test['currency'])
        self.assertTrue(user.check_password(self.user_test['password']))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        for email in self.sample_email:
            user = get_user_model().objects.create_user(email[0], 'test123')

            self.assertEqual(user.email, email[1])

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """
        user = get_user_model().objects.create_superuser(
            email=self.user_test['email'],
            password=self.user_test['password'],
            name=self.user_test['name'],
            phone_number=self.user_test['phone_number'],
            language=self.user_test['language'],
            currency=self.user_test['currency']
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, self.user_test['email'])
        self.assertEqual(user.name, self.user_test['name'])
        self.assertEqual(user.phone_number, self.user_test['phone_number'])
        self.assertEqual(user.language, self.user_test['language'])
        self.assertEqual(user.currency, self.user_test['currency'])
        self.assertTrue(user.check_password(self.user_test['password']))

    def test_create_service_area(self):
        """
        Test save service area model
        """
        provider = get_user_model().objects.create_user(
            email=self.user_test['email'],
            password=self.user_test['password'],
            name=self.user_test['name'],
            phone_number=self.user_test['phone_number'],
            language=self.user_test['language'],
            currency=self.user_test['currency']
        )

        service_area = ServiceArea.objects.create(
            name='Test Service Area',
            polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            description='Test Service',
            price=10,
            provider=provider
        )

        self.assertEqual(service_area.name, 'Test Service Area')
        self.assertEqual(service_area.description, 'Test Service')
        self.assertEqual(service_area.provider, provider)
        self.assertEqual(service_area.price, 10)

    def test_service_area_model_invalid_polygon(self):
        """
        Test service area model with invalid polygon
        """
        provider = get_user_model().objects.create_user(
            email=self.user_test['email'],
            password=self.user_test['password'],
            name=self.user_test['name'],
            phone_number=self.user_test['phone_number'],
            language=self.user_test['language'],
            currency=self.user_test['currency']
        )

        with self.assertRaises(ValueError):
            ServiceArea.objects.create(
                name='Test Service Area',
                polygon=Polygon(((0, 0))),
                description='Test Service',
                price=10,
                provider=provider
            )

        with self.assertRaises(ValueError):
            ServiceArea.objects.create(
                name='Test Service Area',
                polygon=Polygon(((0, 0), (1, 0))),
                description='Test Service',
                price=10,
                provider=provider
            )

    def test_service_area_get_providers_from_lat_lng(self):
        """
        Test get providers from lat lng
        """
        polygons = [
            Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            Polygon(((0, 0), (0, 2), (2, 2), (2, 0), (0, 0))),
            Polygon(((-1, 0), (-1, 5), (4, 5), (4, 0), (-1, 0)))
        ]

        lat_lng = [
            Point(0.5, 0.5),
            Point(-0.5, 0.5),
            Point(0.000001, 1.5)
        ]

        providers = []
        service_areas = []
        service_area_from_lat_lng = []
        # Create Service Areas w/ their provider
        for i in range(3):
            providers.append(
                get_user_model().objects.create_user(
                    email=f'{i}{self.user_test["email"]}',
                    password=self.user_test['password'],
                    name=f'{i}{self.user_test["name"]}',
                    phone_number=f'{i}{self.user_test["phone_number"]}',
                    language=self.user_test['language'],
                    currency=self.user_test['currency']
                )
            )
            service_areas.append(
                ServiceArea.objects.create(
                    name=f'Test Service Area provider{i}',
                    polygon=polygons[i],
                    description=f'Test Service provider{i}',
                    price=10+i,
                    provider=providers[-1]
                )
            )
        # Filter service areas from lat lng
        for l_l in lat_lng:
            service_area_from_lat_lng.append(
                ServiceArea.objects.filter(
                    polygon__contains=l_l
                ).order_by('provider__email')
            )

        self.assertEqual(3, service_area_from_lat_lng[0].count())
        for i in range(3):
            self.assertEqual(
                service_area_from_lat_lng[0][i].provider,
                providers[i]
            )
            self.assertEqual(
                service_area_from_lat_lng[0][i],
                service_areas[i]
            )

        self.assertEqual(1, service_area_from_lat_lng[1].count())
        self.assertEqual(service_areas[-1], service_area_from_lat_lng[1][0])
        self.assertEqual(providers[-1], service_area_from_lat_lng[1][0].provider)

        self.assertEqual(2, service_area_from_lat_lng[2].count())
        self.assertEqual(service_areas[1], service_area_from_lat_lng[2][0])
        self.assertEqual(service_areas[2], service_area_from_lat_lng[2][1])
        self.assertEqual(providers[1], service_area_from_lat_lng[2][0].provider)
        self.assertEqual(providers[2], service_area_from_lat_lng[2][1].provider)

    def test_service_area_get_no_providers_from_lat_lng(self):
        """
        Test get providers from lat lng with no provider
        """
        lat_lng = Point(120, 120)
        provider = get_user_model().objects.create_user(
            email=self.user_test["email"],
            password=self.user_test['password'],
            name=self.user_test["name"],
            phone_number=self.user_test["phone_number"],
            language=self.user_test['language'],
            currency=self.user_test['currency']
        )

        ServiceArea.objects.create(
            name='Test Service Area provider',
            polygon=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))),
            description='Test Service provider',
            price=10,
            provider=provider
        )

        self.assertEqual(
            0,
            ServiceArea.objects.filter(polygon__contains=lat_lng).count()
        )
