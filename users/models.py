from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import UserManager


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('instructor', 'Преподаватель'),
        ('student', 'Студент'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
