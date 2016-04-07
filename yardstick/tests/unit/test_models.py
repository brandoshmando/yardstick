from django.test import TestCase

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
