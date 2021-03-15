
from django.conf import settings
from django.contrib import admin
from django.urls import path,  include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='hello_page/index.html')),
    path('auth/', include('users.urls')),
    path('task/', include('tasks.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls')), ]
