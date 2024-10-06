from django import forms
from .models import Evenement, Lieu

class EvenementForm(forms.ModelForm):
    type_replique_autorisee = forms.MultipleChoiceField(
        choices=Evenement.REPLIQUE_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    lieu = forms.ModelChoiceField(
        queryset=Lieu.objects.filter(actif=True),
        required=False,
        empty_label="Sélectionnez un lieu",
        widget=forms.Select(attrs={'id': 'id_lieu'})
    )

    class Meta:
        model = Evenement
        fields = [
            'type_evenement', 'nom', 'description', 'date_heure', 'lieu', 'adresse',
            'nb_joueurs_max', 'nb_joueurs_min', 'freelance', 'locations', 'repas',
            'prix_freelance', 'prix_location', 'prix_repas', 'puissance_max_joule', 'type_replique_autorisee'
        ]
        widgets = {
            'date_heure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EvenementForm, self).__init__(*args, **kwargs)

        # Ajouter l'option "autre" manuellement
        lieux = list(self.fields['lieu'].queryset)
        self.fields['lieu'].choices = [(None, "Sélectionnez un lieu")] + [(lieu.id, lieu.nom_propre) for lieu in lieux] + [('autre', 'Autre')]

        if self.instance and self.instance.pk:
            self.fields['type_replique_autorisee'].initial = self.instance.get_type_replique_autorisee()
            if self.instance.lieu and self.instance.lieu != 'autre':
                self.fields['adresse'].initial = self.instance.lieu.adresse_postale or self.instance.lieu.coordonnees_gps
