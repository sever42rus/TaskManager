from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room, RoomPermission, RoomColumn, Task


class RoomPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RoomPermission
        fields = ('id', 'user', 'room', 'edit')

# Сериализаторы комнаты


class RoomSerializer(serializers.ModelSerializer):
    room_permission = RoomPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'room_permission')

    def create(self, validated_data):
        user = self.context['request'].user
        instance = Room.objects.create(**validated_data)
        instance.room_permission.create(user=user, edit=True)
        return instance


# Сериализаторы Для Колоник

class TaskSerializer(serializers.ModelSerializer):
    user_edit = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'text', 'user_edit', 'created_date', 'order')


class ColumnSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=True, read_only=True)

    class Meta():
        model = RoomColumn
        fields = ('id', 'name', 'room', 'task', )

    def validate_room(self, room):
        user = self.context['request'].user
        permission = (user.room_permission.all() &
                      room.room_permission.all()).first()
        if not bool(permission):
            raise serializers.ValidationError("Комната не найдена")
        elif not permission.edit:
            raise serializers.ValidationError(
                "Нет разрешения на редактирование")
        else:
            return room


class ColumnEditSerializer(serializers.ModelSerializer):

    class Meta():
        model = RoomColumn
        fields = ('id', 'name',)

# Сериализаторы для Тасков


class TaskFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'text', 'room_column')


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'text', 'room_column')

    def validate_room_column(self, column):
        user = self.context['request'].user
        permission = (user.room_permission.all() &
                      column.room.room_permission.all()).first()
        if not bool(permission):
            raise serializers.ValidationError("Колонка не найдена.")
        else:
            return column

    def create(self, validated_data):
        user = self.context['request'].user
        max_order = Task.objects.filter(
            room_column=validated_data['room_column']).order_by('-order').first()

        instance = super().create(validated_data)
        try:
            instance.order = max_order.order + 1
        except:
            instance.order = 1

        instance.user_edit = user
        instance.save()
        return instance


class TaskEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'text',)
