from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """A custom user model.

    User model with custom required fields (in AbstractUser, them are
    username and password). In this model, all fields are required
    except profile_picture.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name=_('Имя пользователя'),
        max_length=32,
        unique=True,
        db_index=True,
        validators=[username_validator],
    )
    email = models.EmailField(verbose_name=_('E-Mail'), unique=True)
    first_name = models.CharField(verbose_name=_('Имя'), max_length=64)
    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=64)
    profile_picture = models.ImageField(
        verbose_name=_('Фотография'),
        upload_to='users/profile_pictures',
        blank=True
    )
    is_staff = models.BooleanField(
        verbose_name=_('Статус администратора'),
        default=False,
        help_text=_('Определяет, может ли пользователь войти в админ-панель.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('Статус'),
        default=True,
        help_text=_('Определяет, является ли пользователь активным.'),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Дата регистрации'),
        default=timezone.now,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('username',)

    def __str__(self):
        return f'{self.username} ({self.email})'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
