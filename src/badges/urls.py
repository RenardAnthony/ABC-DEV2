from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_badges, name='manage_badges')
]
