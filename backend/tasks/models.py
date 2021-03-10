from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название комнаты')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
        ordering = ['name', ]

    def __str__(self):
        return self.name


class RoomPermission(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='room_permission')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='room_permission')
    edit = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Разрешения на комнату'
        verbose_name_plural = 'Разрешения на комнаты'
        unique_together = [['room', 'user']]


class RoomColumn(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название колонки')
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             verbose_name='Название комнаты', related_name='room_column')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.room, self.name)

    class Meta:
        verbose_name = 'Колонки на комнате'
        verbose_name_plural = 'Колонки на комнатвх'
        ordering = ['created_date', ]


class Task(models.Model):
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.CharField(max_length=512, verbose_name='Текст')
    room_column = models.ForeignKey(RoomColumn, on_delete=models.CASCADE,
                                    verbose_name='Колонка', related_name='task')
    user_edit = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.room_column, self.title)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-created_date', ]
