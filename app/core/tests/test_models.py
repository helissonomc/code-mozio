"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


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
