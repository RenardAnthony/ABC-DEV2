from django.urls import path
from .views import create_gun, update_gun, delete_gun
from . import views

urlpatterns = [
    path('add/', create_gun, name='create_gun'),
    path('update/<int:pk>/', update_gun, name='update_gun'),
    path('delete/<int:pk>/', delete_gun, name='delete_gun'),
    path('verifier/<int:replique_id>/', views.verifier_replique, name='verifier_replique'),
]
