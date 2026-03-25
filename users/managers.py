from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели CustomUser.
    Позволяет создавать пользователей и суперпользователей,
    используя email как основной идентификатор.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя.
        """
        if not email:
            raise ValueError('Email обязателен для пользователя')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя (администратора).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin') # Явно задаём роль администратора

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
