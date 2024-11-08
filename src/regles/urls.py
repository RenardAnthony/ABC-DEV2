from django.urls import path
from . import views

urlpatterns = [
    path('', views.regles_general, name="regles_general"),
]
