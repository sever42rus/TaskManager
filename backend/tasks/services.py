from django.db.models import Avg
from .models import Task


class TaskMovingColumn():

    def __init__(self, data, request):
        self.request = request
        self.task = data['what_task']
        self.column = data['where_column']

    def moving(self):
        Task.objects.filter(
            pk=self.task.id,
        ).update(
            room_column=self.column.id,
            user_edit=self.request.user,
            order=1,
        )


class TaskMovingTask():

    def __init__(self, data, request):
        self.request = request
        self.what_task = data['what_task']
        self.where_task = data['where_task']

    def moving(self):
        if self.what_task.room_column == self.where_task.room_column:
            self.moving_inner_column()
        else:
            new_order = self.new_order()
            if self.where_task.order == new_order:
                self.moving_end_column(new_order+1)
            else:
                self.moving_end_column(new_order)

    def moving_inner_column(self):
        Task.objects.filter(pk=self.what_task.pk).update(
            order=self.where_task.order)
        Task.objects.filter(pk=self.where_task.pk).update(
            order=self.what_task.order)

    def new_order(self):
        return Task.objects.filter(
            room_column=self.where_task.room_column,
            order__gte=self.where_task.order,
        )[:2].aggregate(
            order_avg=Avg('order')
        ).setdefault('order_avg')

    def moving_end_column(self, new_order):
        Task.objects.filter(
            pk=self.what_task.pk,
            room_column__room__room_permission__user=self.request.user,
        ).update(
            room_column=self.where_task.room_column,
            order=new_order
        )
