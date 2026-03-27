from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Section, Material

User = get_user_model()

class CoursesAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        self.instructor = User.objects.create_user(username='instructor', email='instructor@example.com', password='instructor')
        self.student = User.objects.create_user(username='student', email='student@example.com', password='student')
        self.section = Section.objects.create(title='Test Section', owner=self.instructor)
        self.material = Material.objects.create(
            title='Test Material',
            content='Content',
            section=self.section,
            owner=self.instructor,
        )

    def test_section_crud(self):
        self.client.force_authenticate(user=self.instructor)
        data = {'title': 'New Section'}
        response = self.client.post('/courses/sections/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
