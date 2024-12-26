from django import forms
from .models import Gun
from django.forms.widgets import ClearableFileInput

class GunForm(forms.ModelForm):
    class Meta:
        model = Gun
        fields = ['replica_type', 'name', 'photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }

    photo = forms.ImageField(
        widget=ClearableFileInput(attrs={
            'class': 'custom-file-input',  # Classe CSS personnalisée
        }),
        required=False
    )

    def clean_photo(self):
        image = self.cleaned_data.get('photo')
        if image:
            if not image.name.endswith(('png', 'jpg', 'jpeg')):
                raise forms.ValidationError('Seuls les formats .png, .jpg et .jpeg sont autorisés.')
            if image.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError('L\'image ne peut pas dépasser 2MB.')
        return image