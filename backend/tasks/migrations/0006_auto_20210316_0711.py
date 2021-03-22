# Generated by Django 3.1.7 on 2021-03-16 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210315_1029'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='task',
            name='tasks_task_room_co_329c70_idx',
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['order', 'room_column'], name='tasks_task_order_6dd509_idx'),
        ),
    ]