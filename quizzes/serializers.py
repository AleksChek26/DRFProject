from rest_framework import serializers
from .models import Test, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'answers']


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'passing_score', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        test = Test.objects.create(**validated_data)

        for q_data in questions_data:
            answers_data = q_data.pop('answers')
            question = Question.objects.create(test=test, **q_data)
            for a_data in answers_data:
                Answer.objects.create(question=question, **a_data)

        return test

class SubmitAnswerSerializer(serializers.Serializer):
    """
    Сериализатор для отправки ответов студента.
    Принимает список объектов вида: {question_id: ..., selected_answers: [...] }
    """
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )
