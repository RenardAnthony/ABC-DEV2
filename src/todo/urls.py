from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('archive/<int:task_id>/', views.archive_task, name='archive_task'),  # Route pour archiver une tâche
    path('archived/', views.archived_tasks, name='archived_tasks'),  # Route pour afficher les tâches archivées
]
