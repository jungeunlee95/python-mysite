from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('list/<int:page>', views.list, name='list'),
    path('list/', views.list, name='list'),
    path('writeform', views.writeform, name='writeform'),
    path('writeform/<int:no>', views.writeform, name='reply_writeform'),
    path('write', views.write, name='write'),
    path('<int:no>', views.view, name='view'),
    path('modify/<int:no>', views.modifyform, name='modifyform'),
    path('modify', views.modify, name='modify'),
    path('delete/<int:no>', views.delete, name='delete'),
]