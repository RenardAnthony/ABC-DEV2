# account/urls.py

from django.urls import path
from .views import (
    signup, update_user, login_view, logout_view, profile, list_user, delete_user, verify_email, test,
    CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView,
    ChangeEmailView, ConfirmEmailChangeView
)
from django.views.generic import TemplateView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('update-user/', update_user, name='update_user'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/<int:user_id>/', profile, name="user_profile"),
    path('liste-utilisateur/', list_user, name="list_user"),
    path('delete-user/', delete_user, name="delete_user"),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('', login_view, name='login'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/change_email/', ChangeEmailView.as_view(), name='change_email'),
    path('profile/confirm_email_change/<uidb64>/<token>/', ConfirmEmailChangeView.as_view(), name='confirm_email_change'),
    path('profile/email_change_done/', TemplateView.as_view(template_name="account/email_change_done.html"), name='email_change_done'),
    path('profile/email_change_complete/', TemplateView.as_view(template_name="account/email_change_complete.html"), name='email_change_complete'),
    path('profile/email_change_invalid/', TemplateView.as_view(template_name="account/email_change_invalid.html"), name='email_change_invalid'),

    path('test/', test, name="test"),
]
