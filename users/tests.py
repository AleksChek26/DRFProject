from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CustomUser


class UsersAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='admin'
        )

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'student'
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {'email': 'admin@example.com', 'password': 'admin'}
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
