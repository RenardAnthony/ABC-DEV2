from django.urls import path
from .views import update_user_profile, populate_role_permissions


urlpatterns = [
    path('update/', update_user_profile, name='update_user_profile'),
    path('populate_roles/', populate_role_permissions, name='populate_roles'), #profiles/populate_roles/
]
