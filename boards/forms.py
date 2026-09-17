from django import forms
from .models import TaskList, Task

class TaskListForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Columnas (TaskList).
    """
    class Meta:
        model = TaskList
        # Especificamos explícitamente los campos expuestos por seguridad [2]
        fields = ['title', 'position']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nombre de la columna (ej. En Proceso)'}),
            'position': forms.NumberInput(attrs={'min': 0}),
        }


class TaskForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Tareas (Task).
    """
    class Meta:
        model = Task
        # Campos estrictamente seleccionados [2]
        fields = ['title', 'description', 'assigned_to', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título de la tarea'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción detallada...'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # Widget de calendario HTML5
        }