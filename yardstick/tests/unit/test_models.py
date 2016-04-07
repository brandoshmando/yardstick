import uuid
from django.test import TestCase
from django.db import IntegrityError

from yardstick.models import AuthUser

class TestAuthUser(TestCase):
    def test_auth_user_created_email(self):
        user = AuthUser.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.email)
        self.assertIsNone(user.unique_identifier)

    def test_auth_user_created_unque_identifier(self):
        user = AuthUser.objects.create_user(
            unique_identifier=str(uuid.uuid4()),
            password='testpassword'
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.unique_identifier)
        self.assertIsNone(user.email)

    def test_email_unique_identifier_missing(self):
        exception = False
        try:
            user = AuthUser.objects.create_user(
                password='testpassword'
            )
        except ValueError:
            exception = True

        self.assertTrue(exception)

    def test_unique_identifier_not_unique(self):
        exception = False
        identifier = str(uuid.uuid4())

        user = AuthUser.objects.create_user(
            unique_identifier=identifier,
            password='testpassword'
        )
        try:
            AuthUser.objects.create_user(
                unique_identifier=identifier,
                password='testpassword'
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_auth_user_superuser_created_email(self):
        user = AuthUser.objects.create_superuser(
            email='test@example.com',
            password='testpassword'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.email)
        self.assertIsNone(user.unique_identifier)

    def test_auth_user_superuser_created_unque_identifier(self):
        user = AuthUser.objects.create_superuser(
            unique_identifier=str(uuid.uuid4()),
            password='testpassword'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.unique_identifier)
        self.assertIsNone(user.email)

    def test_superuser_email_unique_identifier_missing(self):
        exception = False
        try:
            user = AuthUser.objects.create_superuser(
                password='testpassword'
            )
        except ValueError:
            exception = True

        self.assertTrue(exception)

    def test_superuser_unique_identifier_not_unique(self):
        exception = False
        identifier = str(uuid.uuid4())

        user = AuthUser.objects.create_superuser(
            unique_identifier=identifier,
            password='testpassword'
        )
        try:
            AuthUser.objects.create_superuser(
                unique_identifier=identifier,
                password='testpassword'
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)
