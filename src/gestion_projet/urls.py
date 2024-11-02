from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_d_ensemble, name='vue_d_ensemble'),

    # Listes et détails
    path('taches/', views.taches, name='taches'),
    path('tache/<int:task_id>/', views.tache_detail, name='tache_detail'),
    path('bugs/', views.bugs, name='bugs'),
    path('bug/<int:bug_id>/', views.bug_detail, name='bug_detail'),
    path('bug/resolve/<int:bug_id>/', views.resolve_bug, name='resolve_bug'),


    # Autres pages
    path('live_chat/', views.live_chat, name='live_chat'),
    path('statistiques/', views.statistiques, name='statistiques'),

    # Archivage
    path('tache/<int:task_id>/archiver/', views.archiver_tache, name='archiver_tache'),
    path('<str:item_type>/<int:item_id>/archive/', views.archive_item, name='archive_item'),
    path('bug/<int:bug_id>/resolve/', views.resolve_bug, name='resolve_bug'),
    # Notifications
    path('notifications/lire/', views.marquer_notifications_comme_lues, name='marquer_notifications_comme_lues'),

    # Création et édition dynamiques pour Tâches et Bugs
    path('<str:item_type>/create/', views.manage_item, name='create_item'),
    path('<str:item_type>/<int:item_id>/edit/', views.manage_item, name='edit_item'),

    # Suppression dynamique pour Tâches et Bugs
    path('<str:item_type>/<int:item_id>/delete/', views.delete_item, name='delete_item'),

    # Initialisation des tags
    path('initialiser-tags/', views.initialiser_tags, name='initialiser_tags'),
]
