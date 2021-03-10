from django.contrib import admin
from .models import Room, RoomPermission, RoomColumn, Task
# Register your models here.


class RoomPermissionInLine(admin.TabularInline):
    model = RoomPermission
    extra = 1
    fields = 'user', 'room', 'edit'


class RoomColumnInline(admin.TabularInline):
    model = RoomColumn
    extra = 1
    fields = 'name',


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = 'title', 'text',


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    inlines = [RoomColumnInline, RoomPermissionInLine]


@admin.register(RoomColumn)
class RoomColumnAdmin(admin.ModelAdmin):
    list_display = ('room', 'name', 'id')
    inlines = [TaskInline, ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('room_column', 'title', 'id')
    pass


@admin.register(RoomPermission)
class RoomPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'edit')
    pass
