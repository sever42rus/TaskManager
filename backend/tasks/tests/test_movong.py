from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from users.models import User

from tasks.models import Room, RoomColumn, RoomPermission, Task
from tasks.views import MovongTaskToColumn


class TaskMovingApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email='test1@test.ru', password='123qwezxc'
        )
        self.user2 = User.objects.create(
            email='test2@test.ru', password='123qwezxc'
        )

        self.room1 = Room.objects.create(name='First Room')
        self.room2 = Room.objects.create(name='Two Room')

        RoomPermission.objects.create(
            room=self.room1, user=self.user1, edit=True)
        RoomPermission.objects.create(
            room=self.room1, user=self.user2, edit=False)
        RoomPermission.objects.create(
            room=self.room2, user=self.user1, edit=True)
        RoomPermission.objects.create(
            room=self.room2, user=self.user2, edit=False)

        self.column_room1_1 = RoomColumn.objects.create(
            room=self.room1,
            name='To Make'
        )
        self.column_room1_2 = RoomColumn.objects.create(
            room=self.room1,
            name='Done'
        )
        self.column_room2_1 = RoomColumn.objects.create(
            room=self.room2,
            name='To Make'
        )
        self.column_room2_2 = RoomColumn.objects.create(
            room=self.room2,
            name='Done'
        )

        self.task1 = Task.objects.create(
            title='Task 1',
            text='Task 1',
            room_column=self.column_room1_1,
            user_edit=self.user1,
            order=1,
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            text='Task 2',
            room_column=self.column_room1_1,
            user_edit=self.user1,
            order=2,
        )
        self.task3 = Task.objects.create(
            title='Task 3',
            text='Task 3',
            room_column=self.column_room1_1,
            user_edit=self.user1,
            order=3,
        )
        self.task4 = Task.objects.create(
            title='Task 4',
            text='Task 4',
            room_column=self.column_room1_1,
            user_edit=self.user1,
            order=4,
        )

    def test_moving_task_to_column(self):
        tasks = [self.task1, self.task2]
        factory = APIRequestFactory()
        view = MovongTaskToColumn.as_view()

        first_moving_task = True
        for task in tasks:
            request = factory.put(
                '/task/task/moving/to-column/',
                {
                    'what_task': task.pk,
                    'where_column': self.column_room1_2.pk
                },
                format='json'
            )
            force_authenticate(request, user=self.user1)
            responce = view(request)
            if first_moving_task:
                self.assertEqual(responce.status_code, 200)
                first_moving_task = False
            else:
                self.assertEqual(responce.status_code, 400)

    def test_moving_task_other_room_column(self):
        tasks = [self.task1, self.task2]
        factory = APIRequestFactory()
        view = MovongTaskToColumn.as_view()
        for task in tasks:
            request = factory.put(
                '/task/task/moving/to-column/',
                {
                    'what_task': task.pk,
                    'where_column': self.column_room2_1.pk
                },
                format='json'
            )
            force_authenticate(request, user=self.user1)
            responce = view(request)
            self.assertEqual(responce.status_code, 400)
