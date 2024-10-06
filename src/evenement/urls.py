from django.urls import path
from . import views

urlpatterns = [
    path('', views.evenement_list, name='evenement_list'),
    path('<int:pk>/', views.evenement_detail, name='evenement_detail'),
    path('<int:evenement_id>/inscription/', views.inscription_evenement, name='inscription_evenement'),
    path('<int:evenement_id>/desinscription/', views.desinscription_evenement, name='desinscription_evenement'),
    path('<int:evenement_id>/inscription_ami/', views.inscription_ami, name='inscription_ami'),  # Nouvelle URL
    path('evenement/nouveau/', views.evenement_create_or_update, name='evenement_create'),
    path('evenement/<int:pk>/modifier/', views.evenement_create_or_update, name='evenement_update'),
    path('<int:pk>/delete/', views.evenement_delete, name='evenement_delete'),
    path('<int:pk>/comptabilite/', views.comptabilite_evenement, name='comptabilite_evenement'),
    path('<int:evenement_id>/gestion_participant/<int:inscription_id>/', views.gestion_participant, name='gestion_participant'),


    # Page pour auto complet la bdd des terrains
    path('remplir-bdd-lieux/', views.remplir_bdd_lieux, name='remplir_bdd_lieux'),
    path('lieux/', views.lieu_list, name='lieu_list'),
]
