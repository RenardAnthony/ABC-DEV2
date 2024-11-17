from django import forms
from .models import Badge, UserBadge
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AssignBadgeForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Utilisateur")
    badge = forms.ModelChoiceField(queryset=Badge.objects.all(), label="Badge")

    def assign(self):
        user = self.cleaned_data['user']
        badge = self.cleaned_data['badge']
        UserBadge.objects.create(user=user, badge=badge)
