from django import forms
from .models import Task, BugReport, Tag

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'progress', 'priority', 'tags', 'assigned_to']

    def save(self, commit=True):
        instance = super().save(commit=False)  # Sauvegarde l'instance sans commit
        if commit:
            instance.save()  # Sauvegarde l'instance sans les tags pour le moment
            instance.tags.set(self.cleaned_data['tags'])  # Utilise .set() pour ajouter les tags correctement
        return instance

class BugReportForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = BugReport
        fields = ['title', 'description', 'priority', 'tags', 'assigned_to']

    def save(self, commit=True):
        instance = super().save(commit=False)  # Sauvegarde l'instance sans commit
        if commit:
            instance.save()  # Sauvegarde l'instance sans les tags pour le moment
            instance.tags.set(self.cleaned_data['tags'])  # Utilise .set() pour ajouter les tags correctement
        return instance

class BugResolutionForm(forms.Form):
    resolution_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Décrivez la solution apportée'}),
        label="Description de la résolution",
        required=True
    )