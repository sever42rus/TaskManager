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
        if bool(permission):
            return column

        raise serializers.ValidationError("Колонка не найдена.")

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


class MovongTaskToTaskSerializer(serializers.Serializer):
    what_task = serializers.IntegerField()
    where_task = serializers.IntegerField()


class MovongTaskToColumnSerializer(serializers.Serializer):
    what_task = serializers.IntegerField()
    where_column = serializers.IntegerField()

    def validate_what_task(self, value):
        try:
            user = self.context['user']
            return Task.objects.prefetch_related('room_column__room').get(
                pk=value,
                room_column__room__room_permission__user=user,
            )
        except Task.DoesNotExist:
            raise serializers.ValidationError("Перемещаемая задача не найдена")

    def validate_where_column(self, value):
        try:
            user = self.context['user']
            column = RoomColumn.objects.select_related('room').get(
                pk=value,
                room__room_permission__user=user,
            )
            if not column.task.count():
                return column
            else:
                raise serializers.ValidationError(
                    "Перемещение невозможно, переместите на одио из заданий в данной колонке."
                )
        except RoomColumn.DoesNotExist:
            raise serializers.ValidationError("Колонка не найдена")

    def validate(self, data):
        if data['what_task'].room_column.room != data['where_column'].room:
            raise serializers.ValidationError("В комнате нет такой колонки.")
        return data


class MovongTaskToTaskSerializer(serializers.Serializer):
    what_task = serializers.IntegerField()
    where_task = serializers.IntegerField()

    def get_task(self, value):
        user = self.context['user']
        return Task.objects.get(
            pk=value,
            room_column__room__room_permission__user=user,
        )

    def validate_what_task(self, value):
        try:
            return self.get_task(value)
        except:
            raise serializers.ValidationError("Перемещаемая задача не найдена")

    def validate_where_task(self, value):
        try:
            return self.get_task(value)
        except:
            raise serializers.ValidationError("Колонка не найдена")
