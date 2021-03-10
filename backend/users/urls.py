from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from .views import LoginAPI, LogoutAPI

app_name = 'auth'

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),

    path('login-as/<int:user>/',
         staff_member_required(views.login_as), name="login_as"),
]
