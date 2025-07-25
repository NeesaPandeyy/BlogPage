from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class RegisterTest(APITestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username="newuser1",
            email="newuser1@gmail.com",
            password="023015@",
        )

    def test_duplicate_username(self):
        url = reverse("register-api")
        data = {
            "username": "newuser1",
            "email": "newuser12@gmail.com",
            "password1": "023015@",
            "password2": "023015@",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_duplicate_email(self):
        url = reverse("register-api")
        data = {
            "username": "newuser12",
            "email": "newuser1@gmail.com",
            "password1": "023015@",
            "password2": "023015@",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_create_account(self):
        url = reverse("register-api")
        data = {
            "username": "newuserr",
            "email": "newuserr@gmail.com",
            "password1": "023015@",
            "password2": "023015@",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(username="newuserr").exists())

    def test_password_not_match(self):
        url = reverse("register-api")
        data = {
            "username": "newuserr",
            "email": "newuserr@gmail.com",
            "password1": "023015@@",
            "password2": "023015@",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertIn("Passwords do not match.", response.data["non_field_errors"])

        self.assertFalse(User.objects.filter(username="newuserr").exists())
