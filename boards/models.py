from django.db import models
from django.contrib.auth.models import User  # Modelo de usuario integrado de Django

class Board(models.Model):
    """
    Representa un tablero organizador estilo Trello.
    """
    title = models.CharField(max_length=100, verbose_name="Título del tablero")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="boards", 
        verbose_name="Propietario"
    ) # Si se elimina el usuario, se eliminan sus tableros
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Tablero"
        verbose_name_plural = "Tableros"
        ordering = ['-created_at']

    def __str__(self):
        # Muestra el nombre legible en el panel de administración y consultas
        return self.title


class TaskList(models.Model):
    """
    Representa una columna dentro de un tablero (ej. 'Por hacer', 'En proceso', 'Completado').
    """
    title = models.CharField(max_length=50, verbose_name="Nombre de la columna")
    board = models.ForeignKey(
        Board, 
        on_delete=models.CASCADE, 
        related_name="lists", 
        verbose_name="Tablero"
    )
    position = models.PositiveIntegerField(default=0, verbose_name="Orden/Posición")

    class Meta:
        verbose_name = "Lista de tareas"
        verbose_name_plural = "Listas de tareas"
        ordering = ['position']

    def __str__(self):
        return f"{self.title} ({self.board.title})"


class Task(models.Model):
    """
    Representa una tarea individual dentro de una columna/lista [3].
    """
    # Opciones de prioridad para la tarea
    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título de la tarea")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    task_list = models.ForeignKey(
        TaskList, 
        on_delete=models.CASCADE, 
        related_name="tasks", 
        verbose_name="Columna/Lista"
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_tasks", 
        verbose_name="Asignado a"
    ) # Si se elimina el usuario, la tarea queda sin asignar pero no se borra
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='MEDIUM', 
        verbose_name="Prioridad"
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Fecha límite")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['due_date', '-priority']

    def __str__(self):
        return self.title

# Create your models here.
