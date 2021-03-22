from django.db.models import Avg, OuterRef, Subquery, F

from rest_framework import viewsets, generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, RoomColumn, Task
from .permissions import (
    UserRoomEdit,
    UserColumnEdit
)
from .serializers import (
    TaskFormSerializer,
    TaskCreateSerializer,
    TaskEditSerializer,
    RoomSerializer,
    ColumnSerializer,
    ColumnEditSerializer,
    MovongTaskToColumnSerializer,
    MovongTaskToTaskSerializer
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
        return Response(
            RoomSerializer(instance=Room(),
                           context=self.get_serializer_context()).data
        )


class EditUserRooms(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, UserRoomEdit]
    queryset = Room.objects.all()

# Колонки в комнатах


class ListUserRoomColumn(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ColumnSerializer

    def get_queryset(self):
        return RoomColumn.objects.prefetch_related(
            'task', 'task__user_edit'
        ).filter(
            room__room_permission__user=self.request.user,
            room=self.kwargs['room_pk']
        )


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
    permission_classes = [IsAuthenticated, UserColumnEdit]
    serializer_class = ColumnEditSerializer
    queryset = RoomColumn.objects.all()


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
        return Task.objects.filter(
            room_column__room__room_permission__user=user
        )


class MovongTaskToColumn(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        serializer = MovongTaskToColumnSerializer(
            data=request.data,
            context={'user': request.user}
        )
        if serializer.is_valid():
            Task.objects.filter(
                pk=serializer.validated_data['what_task'].id,
            ).update(
                room_column=serializer.validated_data['where_column'].id,
                user_edit=request.user,
                order=1,
            )
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovongTaskToTask(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        serializer = MovongTaskToTaskSerializer(
            data=request.data,
            context={'user': request.user}
        )
        if serializer.is_valid():
            what_task = serializer.validated_data['what_task']
            where_task = serializer.validated_data['where_task']

            if what_task.room_column == where_task.room_column:
                Task.objects.filter(pk=what_task.pk).update(
                    order=where_task.order)
                Task.objects.filter(pk=where_task.pk).update(
                    order=what_task.order)
            else:
                what_task_new_order = Task.objects.filter(
                    room_column=where_task.room_column,
                    order__gte=where_task.order,
                )[:2].aggregate(
                    order_avg=Avg('order')
                ).setdefault('order_avg')
                if where_task.order == what_task_new_order:
                    Task.objects.filter(
                        pk=what_task.pk,
                        room_column__room__room_permission__user=user,
                    ).update(
                        room_column=where_task.room_column,
                        order=where_task.order+1
                    )
                else:
                    Task.objects.filter(
                        pk=what_task.pk,
                        room_column__room__room_permission__user=user,
                    ).update(
                        room_column=where_task.room_column,
                        order=what_task_new_order
                    )
            return Response(status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
