from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class LoginTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",email="testuser@gmail.com",password="023015@"
        )

    def test_login_user(self):
        url = reverse('login-api')
        data = {
            'username':'testuser',
            'password':'023015@',
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn("Login successful", response.data['message'])

    def test_user_cannot_login_without_data(self):
        url = reverse('login-api')
        response = self.client.post(url)
        self.assertEqual(response.status_code,400)

    def test_login_with_incorrect_username(self):
        url = reverse('login-api')
        data = {
            'username':'testinguser',
            'password':'023015@',
        }
        response = self.client.post(url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn("Invalid data", str(response.data['non_field_errors']))


    def test_login_with_incorrect_password(self):
        url = reverse('login-api')
        data = {
            'username':'testuser',
            'password':'12345@',
        }
        response = self.client.post(url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn("Invalid data", str(response.data['non_field_errors']))




    
   