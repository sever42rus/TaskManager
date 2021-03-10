from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, RoomColumn, Task
from .serializers import (
    TaskFormSerializer,
    TaskCreateSerializer,
    TaskEditSerializer,
    TaskMovingSerializer,
    RoomSerializer,
    ColumnSerializer,
    ColumnEditSerializer
)


# Комнаты


class ListUserRooms(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(room_permission__user=self.request.user)


class FormUserRooms(viewsets.GenericViewSet, generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RoomSerializer

    def create_form_details(self, request, *args, **kwargs):
        return Response(RoomSerializer(instance=Room(), context=self.get_serializer_context()).data)


class EditUserRooms(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(room_permission__user=self.request.user, room_permission__edit=True)

# Колонки в комнатах


class ListUserRoomColumn(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ColumnSerializer

    def get_queryset(self):
        return RoomColumn.objects.filter(room__room_permission__user=self.request.user, room=self.kwargs['room_pk'])


class FormUserRoomColumn(viewsets.GenericViewSet, generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ColumnSerializer

    def create_form_details(self, request, *args, **kwargs):
        room = Room.objects.filter(pk=self.kwargs['room_pk']).first()
        return Response(
            ColumnSerializer(
                instance=RoomColumn(room=room),
                context=self.get_serializer_context()).data
        )


class EditUserRoomColumn(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ColumnEditSerializer

    def get_queryset(self):
        return RoomColumn.objects.filter(
            room__room_permission__user=self.request.user,
            room__room_permission__edit=True,
            room=self.kwargs['room_pk']
        )


# Таски


class FormTask(viewsets.GenericViewSet, generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskCreateSerializer

    def create_form_details(self, request, *args, **kwargs):
        column = RoomColumn.objects.filter(
            pk=self.kwargs['column_pk'],
            room__room_permission__user=self.request.user,).first()
        if column:
            return Response(
                TaskFormSerializer(
                    instance=Task(room_column=column),
                    context=self.get_serializer_context()).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class EditTask(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskEditSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(room_column__room__room_permission__user=user)


class MovongTask(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskMovingSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(room_column__room__room_permission__user=user)
