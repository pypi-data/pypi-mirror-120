from django.db import IntegrityError
from django.test import TestCase

from ..managers import UserManager
from ..models import User


class UserManagerTestCase(TestCase):

    def setUp(self):
        self.manager = UserManager()
        self.manager.model = User

    def test_create_user(self):
        email = 'user@test.email'
        password = 'secret'
        user = self.manager.create_user(email, password)
        expected_user = User.objects.get(email=email)

        # Assertions
        self.assertEqual(user.id, expected_user.id)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user__existing_email(self):
        existing_user = User.objects.create_user(email='user@test.email',
                                                 password='secret')
        new_user = None
        new_email = 'user@test.email'
        password = 'secret'

        with self.assertRaises(Exception) as raised:
            new_user = self.manager.create_user(new_email, password)

        # Assertions
        self.assertEqual(type(raised.exception), IntegrityError)
        self.assertIsNone(new_user)

    def test_create_superuser(self):
        email = 'user@test.email'
        password = 'secret'
        user = self.manager.create_superuser(email, password)
        expected_user = User.objects.get(email=email)

        # Assertions
        self.assertEqual(user.id, expected_user.id)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
