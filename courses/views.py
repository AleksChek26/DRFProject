from rest_framework import viewsets, permissions
from .models import Section, Material
from .serializers import SectionSerializer, MaterialSerializer
from .permissions import IsOwnerOrAdmin

class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Section.objects.all()
        return Section.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Material.objects.all()
        return Material.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
