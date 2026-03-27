from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectionViewSet, MaterialViewSet

app_name = 'courses'

router = DefaultRouter()
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'materials', MaterialViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
]
