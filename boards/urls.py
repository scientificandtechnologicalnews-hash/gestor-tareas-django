# boards/urls.py

from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    # Rutas de Tableros
    path('', views.BoardListView.as_view(), name='board_list'),
    path('board/new/', views.BoardCreateView.as_view(), name='board_create'),
    path('board/<int:pk>/', views.BoardDetailView.as_view(), name='board_detail'),

    # Rutas de Columnas (TaskList)
    path('board/<int:board_pk>/list/add/', views.TaskListCreateView.as_view(), name='list_create'),
    path('list/<int:pk>/edit/', views.TaskListUpdateView.as_view(), name='list_update'),
    path('list/<int:pk>/delete/', views.TaskListDeleteView.as_view(), name='list_delete'),

    # Rutas de Tareas (Task)
    path('list/<int:list_pk>/task/add/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # Ruta AJAX para mover tareas mediante Drag & Drop
    path('task/move/', views.task_move_view, name='task_move'),
]