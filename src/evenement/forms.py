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
        required=True,
        empty_label="Sélectionnez un lieu",
        widget=forms.Select(attrs={'id': 'id_lieu'})
    )

    repas = forms.ChoiceField(
        choices=Evenement.REPAS_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    # Autres champs du formulaire
    adresse = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    puissance_max_joule = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        initial=2.00,
        label="Puissance maximale autorisée (en joules)"
    )

    class Meta:
        model = Evenement
        fields = [
            'type_evenement', 'nom', 'description', 'date_heure', 'lieu',
            'nb_joueurs_max', 'nb_joueurs_min', 'freelance', 'locations', 'repas',
            'prix_freelance', 'prix_location', 'prix_repas', 'puissance_max_joule', 'type_replique_autorisee'
        ]
        widgets = {
            'date_heure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EvenementForm, self).__init__(*args, **kwargs)

        lieux = list(self.fields['lieu'].queryset)
        self.fields['lieu'].widget.choices = [(lieu.id, lieu.nom_propre) for lieu in lieux] + [('autre', 'Autre')]

        self.fields['nom'].widget.attrs.update({'placeholder': 'Entrez le nom de l\'événement ou de la partie'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description de l\'événement.'})

        if self.instance and self.instance.pk:
            self.fields['type_replique_autorisee'].initial = self.instance.get_type_replique_autorisee()
            if self.instance.lieu:
                self.fields['adresse'].initial = self.instance.lieu.adresse_postale or self.instance.lieu.coordonnees_gps

class LieuForm(forms.ModelForm):
    class Meta:
        model = Lieu
        fields = ['identifiant', 'nom_propre', 'note', 'actif', 'adresse_postale', 'coordonnees_gps', 'description_publique', 'taille']
