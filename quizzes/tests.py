from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Material, Section
from quizzes.models import Test, Question, Answer
from users.models import CustomUser


class TestQuizWithoutFixtures(APITestCase):

    def setUp(self):
        """Создаём базовые объекты для тестов"""
        # Создаём пользователей
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.instructor = CustomUser.objects.create_user(
            username='instructor',
            email='instr@example.com',
            password='password123',
            role='instructor'
        )
        self.student = CustomUser.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123',
            role='student'
        )

        # Создаём раздел с владельцем
        self.section = Section.objects.create(
            title="Тестовый раздел",
            description="Описание раздела",
            owner=self.instructor
        )

        # Создаём материал, указывая раздел
        self.material = Material.objects.create(
            title="Основы Python",
            content="Текст материала",
            owner=self.instructor,
            section=self.section
        )

        # Создаём тест с вопросами и ответами
        self.test = Test.objects.create(
            title="Тест по Python",
            material=self.material,
            owner=self.instructor,
            passing_score=60
        )

        # Вопрос 1 (Один правильный ответ)
        self.q1 = Question.objects.create(text="2 + 2?", test=self.test, order=1)
        self.a1_correct = Answer.objects.create(
            text="4", is_correct=True, question=self.q1, order=1
        )
        Answer.objects.create(text="5", is_correct=False, question=self.q1, order=2)

        # Вопрос 2 (Множественный выбор)
        self.q2 = Question.objects.create(
            text="Какие типы неизменяемые?", test=self.test, order=2
        )
        self.a2_correct1 = Answer.objects.create(
            text="int", is_correct=True, question=self.q2, order=1
        )
        self.a2_correct2 = Answer.objects.create(
            text="str", is_correct=True, question=self.q2, order=2
        )
        Answer.objects.create(text="list", is_correct=False, question=self.q2, order=3)

    def test_instructor_can_create_test(self):
        """Преподаватель может создать тест для своего материала."""
        self.client.force_authenticate(user=self.instructor)
        url = reverse('test-list')

        data = {
            "title": "Новый тест",
            "material": self.material.id,
            "passing_score": 70,
            "questions": [
                {
                    "text": "Новый вопрос?",
                    "order": 1,
                    "answers": [
                        {"text": "Да", "is_correct": True, "order": 1},
                        {"text": "Нет", "is_correct": False, "order": 2}
                    ]
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Test.objects.filter(title="Новый тест").exists())

    def test_instructor_sees_only_own_tests(self):
        """Преподаватель видит в списке только свои тесты."""
        # Создаём второго преподавателя и его раздел
        instructor2 = CustomUser.objects.create_user(
            username='instructor2',
            email='i2@example.com',
            password='password123',
            role='instructor'
        )

        section2 = Section.objects.create(
            title="Раздел 2",
            description="Второй раздел",
            owner=instructor2
        )

        material2 = Material.objects.create(
            title="Материал 2",
            content="Текст материала 2",
            owner=instructor2,
            section=section2
        )

        Test.objects.create(title="Тест другого препода", material=material2, owner=instructor2)

        self.client.force_authenticate(user=self.instructor)
        url = reverse('test-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Должен видеть только 1 тест (свой)

    def test_student_cannot_create_test(self):
        """Студент не может создать тест."""
        self.client.force_authenticate(user=self.student)
        url = reverse('test-list')

        data = {
            "title": "Попытка студента",
            "material": self.material.id,
            "passing_score": 60
        }

        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])


    def test_submit_test_success(self):
        """Студент успешно проходит тест, выбрав все правильные ответы."""
        self.client.force_authenticate(user=self.student)
        # Прямой URL вместо reverse (если имя маршрута не настроено)
        url = f'/api/tests/{self.test.id}/submit/'

        data = {
            "answers": [
                {"question_id": self.q1.id, "answer_ids": [self.a1_correct.id]},
                {"question_id": self.q2.id, "answer_ids": [self.a2_correct1.id, self.a2_correct2.id]}
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data.get('score', 0), 80)  # Оценка должна быть высокой

    def test_submit_test_partial_success(self):
        """Студент проходит тест частично (50%)."""
        self.client.force_authenticate(user=self.student)
        url = f'/api/tests/{self.test.id}/submit/'

        data = {
            "answers": [
                {"question_id": self.q1.id, "answer_ids": [self.a1_correct.id]},  # Правильный ответ
                {"question_id": self.q2.id, "answer_ids": [self.a2_correct1.id]}  # Частичный ответ
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        score = response.data.get('score', 0)
        self.assertGreaterEqual(score, 50)
        self.assertLess(score, 80)
