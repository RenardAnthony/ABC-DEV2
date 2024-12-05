from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_notifications, name='list_notifications'),
    path('mark-as-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
]
