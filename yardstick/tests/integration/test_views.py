import json
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.urlresolvers import reverse

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
