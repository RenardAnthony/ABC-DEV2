from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio_gender', 'choices_gender', 'blood_group', 'avatar', 'bio', 'tel', 'adresse', 'nom', 'prenom']

        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'input-avatar'}),
            'bio': forms.Textarea(attrs={
                'class': 'input-bio',
                'maxlength': '255',
                'rows': 6,
                'placeholder': 'Écris ta biographie ici...'
            }),
            'nom': forms.TextInput(attrs={'class': 'input-box2'}),
            'prenom': forms.TextInput(attrs={'class': 'input-box2'}),
            'choices_gender': forms.Select(attrs={'class': 'input-box2-choice'}),
            'blood_group': forms.Select(attrs={'class': 'input-box2-choice'}),
            'tel': forms.TextInput(attrs={'class': 'input-box2'}),
            'adresse': forms.TextInput(attrs={'class': 'input-box2'}),
        }

    def clean_photo(self):
        image = self.cleaned_data.get('avatar')
        if image:
            if not image.name.endswith(('png', 'jpg', 'jpeg')):
                raise forms.ValidationError('Seuls les formats .png, .jpg et .jpeg sont autorisés.')
            if image.size > 2 * 1024 * 1024:  # Limite de 2MB
                raise forms.ValidationError('L\'image ne peut pas dépasser 2MB.')
        return image
