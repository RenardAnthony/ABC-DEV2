from django import forms
from .models import CustomUser
from datetime import datetime

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label='Nouvelle adresse email', max_length=254)

class CustomUserForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={'placeholder': 'jj/mm/aaaa', 'type': 'date'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['pseudo', 'date_of_birth']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            return self.instance.date_of_birth  # Retourne l'ancienne valeur si le champ est vide
        return date_of_birth