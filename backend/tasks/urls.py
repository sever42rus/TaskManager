from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('room/list/', views.ListUserRooms.as_view()),
    path('room/form/',
         views.FormUserRooms.as_view({'get': 'create_form_details'})),
    path('room/edit/<int:pk>/', views.EditUserRooms.as_view()),

    path('column/list/<int:room_pk>/', views.ListUserRoomColumn.as_view(),),
    path('column/form/<int:room_pk>/',
         views.FormUserRoomColumn.as_view({'get': 'create_form_details'})),
    path('column/edit/<int:pk>/',
         views.EditUserRoomColumn.as_view()),

    # path('column/edit/<int:room_pk>/<int:pk>/',
    # views.EditUserRoomColumn.as_view()),

    path('task/form/<int:column_pk>/',
         views.FormTask.as_view({'get': 'create_form_details'})),
    path('task/edit/<int:pk>/', views.EditTask.as_view()),
    path('task/moving/', views.MovongTask.as_view())
]
