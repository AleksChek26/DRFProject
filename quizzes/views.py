from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Test
from .serializers import TestSerializer, SubmitAnswerSerializer
from .permissions import IsOwnerOrAdmin


class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Test.objects.all()

        # Преподаватели видят только свои тесты (через владельца материала)
        return Test.objects.filter(material__owner=user)

    def perform_create(self, serializer):
        # При создании теста автоматически назначаем текущего пользователя владельцем
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

        return super().get_permissions()


class SubmitTestView(generics.GenericAPIView):
    """
    Эндпоинт для отправки ответов студента на тест.
    """
    serializer_class = SubmitAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = kwargs.get('pk')

        try:
            test = Test.objects.prefetch_related('questions__answers').get(id=test_id)

            if not test.questions.exists():
                return Response({'error': 'Тест не содержит вопросов.'}, status=status.HTTP_400_BAD_REQUEST)

            correct_answers_count = 0

            # Получаем данные студента из сериализатора (список словарей)
            student_answers_data = serializer.validated_data['answers']

            # Создаем словарь для быстрого поиска ответов студента по id вопроса {question_id: [answer_id1, answer_id2]}
            student_answers_map = {
                item['question_id']: item['selected_answers']
                for item in student_answers_data
                if 'question_id' in item and 'selected_answers' in item
            }

            # Проверяем каждый вопрос в тесте
            for question in test.questions.all():
                selected_ids = student_answers_map.get(question.id, [])

                correct_qs_ids = set(question.answers.filter(is_correct=True).values_list('id', flat=True))
                wrong_qs_selected_ids = set(
                    question.answers.filter(is_correct=False).values_list('id', flat=True)) & set(selected_ids)

                is_fully_correct = (
                        set(selected_ids) == correct_qs_ids
                        and not wrong_qs_selected_ids
                        and len(selected_ids) > 0
                # Хотя бы один ответ выбран (если не multiple choice с пустым правильным ответом)
                )

                if is_fully_correct:
                    correct_answers_count += 1

            questions_count = test.questions.count()
            score_percent = round((correct_answers_count / questions_count) * 100) if questions_count > 0 else 0
            passed = score_percent >= test.passing_score

            return Response({
                'test_id': test.id,
                'total_questions': questions_count,
                'correct_answers': correct_answers_count,
                'score_percent': score_percent,
                'passing_score': test.passing_score,
                'passed': passed,
                'message': 'Тест успешно проверен.'
            }, status=status.HTTP_200_OK)

        except Test.DoesNotExist:
            return Response({'error': 'Тест не найден.'}, status=status.HTTP_404_NOT_FOUND)
