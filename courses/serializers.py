from rest_framework import serializers
from .models import Section, Material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'content', 'section', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']

class SectionSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'owner', 'created_at', 'materials']
        read_only_fields = ['owner', 'created_at']
