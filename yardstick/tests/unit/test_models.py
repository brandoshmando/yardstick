import uuid
from django.test import TestCase
from django.db import IntegrityError
from rest_framework.authtoken.models import Token

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

    def test_auth_user_token_created(self):
        user = AuthUser.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )

        self.assertIsNotNone(Token.objects.get(user=user).key)

    def test_auth_user_superuser_token_created(self):
        user = AuthUser.objects.create_superuser(
            email='test@example.com',
            password='testpassword'
        )

        self.assertIsNotNone(Token.objects.get(user=user).key)

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
            user=self.user
        )
        self.administrator = Administrator.objects.create(
            organization_id=self.organization,
            user=self.user
        )
        self.arbiter = Arbiter.objects.create(
            organization_id=self.organization,
            user=self.user
        )
        self.subject = Subject.objects.create(
            organization_id=self.organization,
            user=self.user
        )

    def test_unique_org_user_combo_manager(self):
        exception = False
        try:
            Manager.objects.create(
                organization_id=self.organization,
                user=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_unique_org_user_combo_administrator(self):
        exception = False
        try:
            Administrator.objects.create(
                organization_id=self.organization,
                user=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_unique_org_user_combo_arbiter(self):
        exception = False
        try:
            Arbiter.objects.create(
                organization_id=self.organization,
                user=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)

    def test_unique_org_user_combo_subject(self):
        exception = False
        try:
            Subject.objects.create(
                organization_id=self.organization,
                user=self.user
            )
        except IntegrityError:
            exception = True

        self.assertTrue(exception)


class TestOrganizationCreate(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_user(
            email='test_first@example.com',
            password='testpassword'
        )

    def test_create_new_org(self):
        name = "Test Name"
        ui = str(uuid.uuid4())
        auth_data = {
            'first_name':'Brando',
            'last_name':'Shmando',
            'email':"test@example.com",
            'password':"testpassword"
        }

        organization = Organization.objects.create_account(
            name=name,
            unique_identifier=ui,
            auth_data=auth_data
        )


        self.assertIsNotNone(organization.managers.first())
        self.assertEqual(organization.managers.all().count(), 1)
        self.assertIsNotNone(organization.managers.first().user)

        self.assertEqual(organization.name, name)
        self.assertEqual(organization.managers.first().user.email, auth_data['email'])
        self.assertEqual(organization.managers.first().unique_identifier, ui)
        self.assertIsNotNone(organization.managers.first().user.password)
        self.assertFalse(organization.managers.first().user.is_staff)

    def test_create_new_org_existing_user(self):
        name = "Test Name"
        ui = str(uuid.uuid4())
        auth_data = {
            'first_name':'Brando',
            'last_name':'Shmando',
            'email':"test_first@example.com",
            'password':"testpassword"
        }

        organization = Organization.objects.create_account(
            name=name,
            unique_identifier=ui,
            auth_data=auth_data
        )

        self.assertIsNotNone(organization.managers.first())
        self.assertEqual(organization.managers.all().count(), 1)
        self.assertIsNotNone(organization.managers.first().user)

        self.assertEqual(organization.managers.first().user, self.user)
        self.assertEqual(organization.managers.first().user.email, auth_data['email'])
