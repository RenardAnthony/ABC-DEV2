from django.urls import path
from .views import manage_gun, delete_gun
from . import views

urlpatterns = [
    path('manage/', manage_gun, name='create_gun'),
    path('manage/<int:pk>/', manage_gun, name='update_gun'),
    path('delete/<int:pk>/', delete_gun, name='delete_gun'),
    path('verifier/<int:replique_id>/', views.verifier_replique, name='verifier_replique'),
    path('calcul_puissance/', views.calcul_puissance, name='calcul_puissance'),

]
