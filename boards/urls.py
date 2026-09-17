from django.urls import path
from . import views

# Definimos el espacio de nombres de la aplicación
app_name = 'boards'

urlpatterns = [
    # Ruta para la lista de tableros
    path('', views.BoardListView.as_view(), name='board_list'),
    
    # Ruta para crear un nuevo tablero
    path('board/new/', views.BoardCreateView.as_view(), name='board_create'),
    
    # Ruta para ver el detalle de un tablero específico (ej. /board/1/)
    path('board/<int:pk>/', views.BoardDetailView.as_view(), name='board_detail'),
]
