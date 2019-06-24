from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('list/<int:page>', views.list, name='list'),
    path('list/', views.list, name='list'),
    path('writeform/<int:page>', views.writeform, name='writeform'),
    path('writeform/<int:no>/<int:page>', views.writeform, name='reply_writeform'),
    path('write/<int:page>', views.write, name='write'),
    path('<int:no>/<int:page>', views.view, name='view'),
    path('modify/<int:no>/<int:page>', views.modifyform, name='modifyform'),
    path('modify/<int:page>', views.modify, name='modify'),
    path('delete/<int:no>/<int:page>', views.delete, name='delete'),
]