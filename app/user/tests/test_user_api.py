"""
Test for the user API
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.payload_create = {
            'email': 'testuserapi@api.com',
            'password': 'testpass',
            'name': 'Test name',
            'phone_number': '+123456789',
            'language': 'en',
            'currency': 'USD'
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        res = self.client.post(CREATE_USER_URL, self.payload_create)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload_create['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        create_user(**self.payload_create)

        res = self.client.post(CREATE_USER_URL, self.payload_create)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = self.payload_create.copy()
        payload['password'] = 'pw'

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)