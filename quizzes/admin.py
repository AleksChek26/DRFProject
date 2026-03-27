from django.contrib import admin
from .models import Test, Question, Answer


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'material', 'owner', 'passing_score')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
