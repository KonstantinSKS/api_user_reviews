from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    USER_ROLES = (
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(role[0]) for role in USER_ROLES),
        choices=USER_ROLES,
        default=USER
    )
    email = models.EmailField('Почта', unique=True, blank=False)

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        constraints = [
            UniqueConstraint(
                fields=['username', 'email'],
                name="pair username/email should be unique"),
            models.CheckConstraint(
                check=~models.Q(username="me"), name="username can't be me"
            )
        ]

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self) -> str:
        return self.username
