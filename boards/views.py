from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Board

class BoardListView(LoginRequiredMixin, ListView):
    """
    Muestra la lista de tableros pertenecientes únicamente al usuario autenticado.
    """
    model = Board
    template_name = 'boards/board_list.html'
    context_object_name = 'boards'

    def get_queryset(self):
        # Filtra los tableros para mostrar solo los del usuario logueado
        return Board.objects.filter(owner=self.request.user)


class BoardDetailView(LoginRequiredMixin, DetailView):
    """
    Muestra el detalle de un tablero específico junto a sus columnas (TaskList) y tareas (Task).
    """
    model = Board
    template_name = 'boards/board_detail.html'
    context_object_name = 'board'


class BoardCreateView(LoginRequiredMixin, CreateView):
    """
    Formulario para crear un nuevo tablero.
    """
    model = Board
    template_name = 'boards/board_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('boards:board_list')

    def form_valid(self, form):
        # Asigna automáticamente al usuario logueado como propietario del tablero
        form.instance.owner = self.request.user
        return super().form_valid(form)

class SignUpView(CreateView):
    """
    Vista encargada del registro de nuevos usuarios en la plataforma.
    Usa el formulario por defecto de Django que gestiona nombre de usuario y contraseña con validaciones.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirige al login tras crear la cuenta con éxito
    template_name = 'registration/register.html'
# Create your views here.
