from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.urls import reverse

from .models import User, UserGroup, UserLog


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'login_as', 'is_active',
                    'is_staff', 'is_superuser',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональные данные', {
         'fields': ('first_name', 'parent_name', 'last_name')}),
        ('Разрешения', {'fields': ('is_active',
                                   'is_staff', 'is_superuser', 'groups',)}),
        ('Информация о входе', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def login_as(self, obj):
        return format_html(
            "<a href='{}' class='btn btn-info' style='padding:1px 3px;'>login</a>",
            reverse('auth:login_as', kwargs={'user': obj.id})
        )
    login_as.short_description = 'Войти под пользователем'


@admin.register(UserGroup)
class UserGroupAdmin(GroupAdmin):
    pass


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = 'action_time', 'user', 'content_type', '__str__',
    raw_id_fields = 'user',
    date_hierarchy = 'action_time'
    list_filter = 'content_type',
