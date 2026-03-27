from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TestViewSet, SubmitTestView

app_name = 'quizzes'

router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls)),

    # Отдельный URL для проверки теста (не через ViewSet!)
    path('test/<int:pk>/submit/', SubmitTestView.as_view(), name='submit-test'),
]