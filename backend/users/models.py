from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.contrib.admin.models import LogEntry
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        user = User(email=email.lower(), is_active=is_active, is_staff=is_staff,
                    is_superuser=is_superuser, date_joined=timezone.now(), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True, error_messages={
                              'unique': 'Пользователь с таким email уже существует'})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    first_name = models.CharField('Имя', max_length=100, null=True)
    last_name = models.CharField('Фамилия', max_length=100, null=True,)
    parent_name = models.CharField('Отчество', max_length=100, null=True,)

    @property
    def fio(self):
        return ' '.join((self.last_name, self.first_name, self.parent_name))

    @property
    def ini(self):
        if not self.first_name or not self.parent_name:
            return self.last_name
        return f'{self.last_name} {self.first_name[0]}.{self.parent_name[0]}.'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserGroup(Group):
    # только для админки

    class Meta:
        proxy = True
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class UserLog(LogEntry):
    # только для админки

    class Meta:
        proxy = True
        verbose_name = 'Действие'
        verbose_name_plural = 'История действий'
