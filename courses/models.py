from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Section(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='materials')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='materials')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
