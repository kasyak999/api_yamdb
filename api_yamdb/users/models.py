from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)
MAX_LENGT_EMAIL = 254
MAX_LENGT_USERNAME = 150


class UserProfile(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(
        unique=True, blank=True, max_length=MAX_LENGT_EMAIL)
    username = models.CharField(
        max_length=MAX_LENGT_USERNAME, blank=True, unique=True)
    role = models.CharField(
        max_length=150, blank=True, default='user', choices=ROLES)
    code = models.TextField(blank=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        """Перевод модели"""

        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
