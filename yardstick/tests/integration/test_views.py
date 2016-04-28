import json
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.urlresolvers import reverse

from yardstick.models import AuthUser

class TestOrganizationPost(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_signup(self):
        data = {
            'name': 'Test Org',
            'first_name':'Brando',
            'last_name':'Craft',
            'email':'test@example.com',
            'password':'testpassword'
        }

        response = self.client.post(reverse('organization-create'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Token.objects.first().key, response.data['token'])


class TestUserAuth(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-auth')
        self.email = "test@example.com"
        self.password = "testpassword"
        self.auth_user = AuthUser.objects.create_user(email=self.email, password=self.password)
        self.token = Token.objects.get(user=self.auth_user)

    def test_successful_signin(self):
        data = {
            "email":self.email,
            "password":self.password
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(user=self.auth_user).key, response.data['token'])

    def test_right_email_wrong_pass(self):
        data = {
            "email": self.email,
            "password":"wrongpass"
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.data['non_field_errors'][0], "Invalid email and/or password combination. Please try again!")

    def test_wrong_email(self):
        data = {
            "email": "fake@example.com",
            "password": self.password
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data.get('token'))
        self.assertEqual(response.data['non_field_errors'][0], "Invalid email and/or password combination. Please try again!")

    def test_invalid_data(self):
        data = {}

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], 'This field is required.')
        self.assertEqual(response.data['email'][0], 'This field is required.')
