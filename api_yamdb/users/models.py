from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

LENGTH_TEXT = 15

USER_ROLE = 'user'
MODER_ROLE = 'moderator'
ADMIN_ROLE = 'admin'

ROLE_CHOICES = (
    ('UR', USER_ROLE,),
    ('MR', MODER_ROLE,),
    ('AR', ADMIN_ROLE,),
)


class User(AbstractUser):
    """Класс пользователей."""
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль',
        choices=ROLE_CHOICES,
        default=USER_ROLE
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:LENGTH_TEXT]

    def is_admin(self):
        return self.role == ADMIN_ROLE

    def is_moderator(self):
        return self.role == MODER_ROLE

    def is_user(self):
        return self.role == USER_ROLE