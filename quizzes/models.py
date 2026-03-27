from django.db import models
from courses.models import Material
from users.models import CustomUser

class Test(models.Model):
    material = models.OneToOneField(
        Material,
        on_delete=models.CASCADE,
        related_name='test',
        verbose_name='Материал'
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name='Владелец'
    )
    title = models.CharField(max_length=255, verbose_name='Название теста')
    passing_score = models.PositiveIntegerField(default=60, verbose_name='Проходной балл (%)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Тест к материалу: {self.material.title}"

class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест'
    )
    text = models.TextField(verbose_name='Текст вопроса')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text
