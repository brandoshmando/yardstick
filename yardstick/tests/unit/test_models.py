import uuid
from django.test import TestCase
from django.db import IntegrityError


from yardstick.models import AuthUser, Organization, Manager, Administrator, Arbiter, Subject

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

    def test_email_not_unique(self):
        exception = False
        email = 'test@example.com'

        user = AuthUser.objects.create_user(
            email=email,
            password='testpassword'
        )
        try:
            AuthUser.objects.create_user(
                email=email,
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


class TestAuthUserManagerOrganizationCombo(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.organization = Organization.objects.create(
            name='Test Org'
        )
        self.manager = Manager.objects.create(
            organization_id=self.organization,
            user_id=self.user
        )
        self.administrator = Administrator.objects.create(
            organization_id=self.organization,
            user_id=self.user
        )
        self.arbiter = Arbiter.objects.create(
            organization_id=self.organization,
            user_id=self.user
        )
        self.subject = Subject.objects.create(
            organization_id=self.organization,
            user_id=self.user
        )

    def test_unique_org_user_combo_manager(self):
        exception = False
        try:
            Manager.objects.create(
                organization_id=self.organization,
                user_id=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_unique_org_user_combo_administrator(self):
        exception = False
        try:
            Administrator.objects.create(
                organization_id=self.organization,
                user_id=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_unique_org_user_combo_arbiter(self):
        exception = False
        try:
            Arbiter.objects.create(
                organization_id=self.organization,
                user_id=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_unique_org_user_combo_subject(self):
        exception = False
        try:
            Subject.objects.create(
                organization_id=self.organization,
                user_id=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)
