from django.urls import path, re_path
from . import views

app_name = 'guestbook'

urlpatterns = [
    path('list', views.list, name='list'),
    path('write', views.write, name='write'),
    re_path(r'^guestbook/delete(?:/(?P<id>\d+))?/$', views.delete, name='delete')
    # path('delete/<int:id>', views.delete, name='delete'),
    # path('delete', views.delete, name='delete'),
]