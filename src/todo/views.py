from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def todo_list(request):
    tasks = Task.objects.filter(archived=False)  # Filtre pour ne pas afficher les tâches archivées
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    remaining_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percentage = (completed_tasks / total_tasks) * 100
        progress_percentage = round(progress_percentage)
    else:
        progress_percentage = 0

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'remaining_tasks': remaining_tasks,
        'progress_percentage': progress_percentage
    }

    return render(request, 'todo/todo_list.html', context)

def archive_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.archived = True
    task.save()
    return redirect('todo_list')

def archived_tasks(request):
    archived_tasks = Task.objects.filter(archived=True)
    context = {
        'tasks': archived_tasks,
    }
    return render(request, 'todo/archived_tasks.html', context)


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('todo_list')
