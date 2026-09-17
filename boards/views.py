from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Board, TaskList, Task
from .forms import TaskListForm, TaskForm

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

# ==========================================
# VISTAS DE COLUMNAS (TaskList)
# ==========================================

class TaskListCreateView(LoginRequiredMixin, CreateView):
    """
    Permite crear una nueva columna asociada a un tablero específico.
    """
    model = TaskList
    form_class = TaskListForm
    template_name = 'boards/tasklist_form.html'

    def form_valid(self, form):
        # Asocia la columna al tablero pasado por la URL validando que pertenezca al usuario logueado
        board = get_object_or_404(Board, pk=self.kwargs['board_pk'], owner=self.request.user)
        form.instance.board = board
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('boards:board_detail', kwargs={'pk': self.kwargs['board_pk']})


class TaskListUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permite editar el nombre o posición de una columna.
    """
    model = TaskList
    form_class = TaskListForm
    template_name = 'boards/tasklist_form.html'

    def get_queryset(self):
        # Restringe la edición a columnas de tableros pertenecientes al usuario
        return TaskList.objects.filter(board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('boards:board_detail', kwargs={'pk': self.object.board.pk})


class TaskListDeleteView(LoginRequiredMixin, DeleteView):
    """
    Elimina una columna y todas sus tareas asociadas.
    """
    model = TaskList
    template_name = 'boards/tasklist_confirm_delete.html'

    def get_queryset(self):
        return TaskList.objects.filter(board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('boards:board_detail', kwargs={'pk': self.object.board.pk})


# ==========================================
# VISTAS DE TAREAS (Task)
# ==========================================

class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Permite crear una nueva tarea dentro de una columna específica.
    """
    model = Task
    form_class = TaskForm
    template_name = 'boards/task_form.html'

    def form_valid(self, form):
        # Valida que la columna pertenezca a un tablero del usuario logueado
        task_list = get_object_or_404(TaskList, pk=self.kwargs['list_pk'], board__owner=self.request.user)
        form.instance.task_list = task_list
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('boards:board_detail', kwargs={'pk': self.object.task_list.board.pk})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permite editar los detalles de una tarea (asignación, prioridad, fecha límite, etc.).
    """
    model = Task
    form_class = TaskForm
    template_name = 'boards/task_form.html'

    def get_queryset(self):
        return Task.objects.filter(task_list__board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('boards:board_detail', kwargs={'pk': self.object.task_list.board.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Elimina una tarea individual.
    """
    model = Task
    template_name = 'boards/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(task_list__board__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('boards:board_detail', kwargs={'pk': self.object.task_list.board.pk})
# Create your views here.
