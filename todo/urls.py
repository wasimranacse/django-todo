from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-todo/', views.create_todo, name='create-todo'),
    path('todo/<id>/', views.todo_details, name='todo'),
    path('todo-delete/<id>/', views.todo_delete, name='todo-delete'),
    path('todo-edit/<id>/', views.edit_todo, name='todo-edit'),
]
