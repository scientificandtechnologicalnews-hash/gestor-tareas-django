from django.contrib import admin
from .models import Board, TaskList, Task

# ==========================================
# CONFIGURACIONES INLINE (Edición anidada)
# ==========================================

class TaskInline(admin.TabularInline):
    """
    Permite ver y editar Tareas directamente desde el formulario de una Lista (TaskList).
    """
    model = Task
    extra = 1  # Filas vacías adicionales para agregar nuevas tareas fácilmente
    fields = ('title', 'assigned_to', 'priority', 'due_date')


class TaskListInline(admin.TabularInline):
    """
    Permite ver y editar Columnas/Listas directamente desde el formulario de un Tablero (Board).
    """
    model = TaskList
    extra = 1  # Muestra 1 columna vacía para agregar rápido
    ordering = ('position',)


# ==========================================
# REGISTRO DE MODELOS PRINCIPALES
# ==========================================

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Configuración del panel para el modelo Board (Tableros).
    """
    list_display = ('title', 'owner', 'created_at')  # Columnas visibles en el listado
    list_filter = ('created_at', 'owner')           # Filtros laterales
    search_fields = ('title', 'description')         # Barra de búsqueda
    inlines = [TaskListInline]                      # Incluye la gestión de columnas anidadas


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    """
    Configuración del panel para el modelo TaskList (Columnas).
    """
    list_display = ('title', 'board', 'position')
    list_filter = ('board',)
    search_fields = ('title',)
    inlines = [TaskInline]                          # Incluye la gestión de tareas anidadas


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Configuración del panel para el modelo Task (Tareas).
    """
    list_display = ('title', 'task_list', 'assigned_to', 'priority', 'due_date', 'created_at')
    list_filter = ('priority', 'due_date', 'task_list__board') # Filtra por prioridad, fecha y tablero
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'                       # Navegación por fechas límite

# Register your models here.
