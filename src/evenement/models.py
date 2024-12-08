from django.db import models
from django.utils import timezone
from account.models import CustomUser
from django.conf import settings
from gun.models import Gun
from django.urls import reverse
from decimal import Decimal
class Evenement(models.Model):
    TYPE_CHOICES = [
        ('Partie', 'Partie'),
        ('Evenement', 'Evenement'),
    ]
    REPLIQUE_CHOICES = [
        ('AEG', 'AEG'),
        ('SMG', 'SMG'),
        ('PA', 'PA'),
        ('POMPE', 'POMPE'),
        ('MG', 'MG'),
        ('DMR', 'DMR'),
        ('AUTRE', 'AUTRE'),
        ('Pas de réplique', 'Pas de réplique'),
    ]

    REPAS_CHOICES = [
        ('Aucun', 'Aucun repas fourni'),
        ('Inclus', 'Repas inclus'),
        ('Apporter', 'Apportez votre propre repas')
    ]

    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_heure = models.DateTimeField()

    # Relation avec le modèle Lieu
    lieu = models.ForeignKey('Lieu', on_delete=models.SET_NULL, null=True, blank=False)  # Lieu obligatoire, mais peut être "null" s'il est supprimé
    adresse_autre = models.CharField(max_length=255, blank=True, null=True, default="")  # Adresse personnalisée

    nb_joueurs_max = models.PositiveIntegerField()
    nb_joueurs_min = models.PositiveIntegerField()
    freelance = models.BooleanField(default=False)
    locations = models.BooleanField(default=False)
    repas = models.CharField(max_length=20, choices=REPAS_CHOICES, default='Aucun')
    prix_freelance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    prix_location = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    prix_repas = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # Limites des répliques
    limite_aeg = models.IntegerField(default=0)
    limite_smg = models.IntegerField(default=0)
    limite_pa = models.IntegerField(default=0)
    limite_pompe = models.IntegerField(default=0)
    limite_mg = models.IntegerField(default=0)
    limite_dmr = models.IntegerField(default=0)
    limite_autre = models.IntegerField(default=0)

    type_replique_autorisee = models.CharField(max_length=200, blank=True)

    #puissance_max_joule = models.PositiveIntegerField(default=2)
    puissance_max_joule = models.DecimalField(max_digits=5, decimal_places=2, default=2.0)

    def __str__(self):
        return self.nom

    # Méthode pour renvoyer les types de répliques sélectionnées sous forme de liste
    def get_type_replique_autorisee(self):
        if self.type_replique_autorisee:
            cleaned_string = self.type_replique_autorisee.strip('[]').replace("'", "")
            return [replique.strip() for replique in cleaned_string.split(',')]
        return []

    # Méthode pour définir les types de répliques sélectionnées
    def set_type_replique_autorisee(self, replique_list):
        self.type_replique_autorisee = ','.join(replique_list)

# Nouveau modèle pour les types de répliques
class RepliqueType(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Inscription(models.Model):

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )  # L'utilisateur inscrit (si c'est un compte existant)

    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)

    repas = models.BooleanField(default=False)
    location = models.BooleanField(default=False)
    besoin_covoiturage = models.BooleanField(default=False)
    offre_covoiturage = models.BooleanField(default=False)

    accepte_regles = models.BooleanField(default=False)
    inscrit_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscriptions_faites'
    )  # L'utilisateur qui a inscrit l'ami
    nom_ami = models.CharField(max_length=100, blank=True)  # Nom de l'ami inscrit (s'il n'a pas de compte)

    date_inscription = models.DateTimeField(auto_now_add=True)

    repliques = models.ManyToManyField('gun.Gun', blank=True) # Ajoutez cette ligne pour les répliques

    paiement_valide = models.BooleanField(default=False)
    chrony_valide = models.BooleanField(default=False)

    replique_ami = models.ForeignKey(Gun, null=True, blank=True, on_delete=models.SET_NULL, related_name='repliques_ami')
    amis_repliques = models.CharField(max_length=255, blank=True)

    # Nouveau champ pour stocker le montant total à payer
    montant_total = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('utilisateur', 'evenement', 'nom_ami')

    def __str__(self):
        if self.utilisateur:
            return f"{self.utilisateur.pseudo} - {self.evenement.nom}"
        return f"{self.nom_ami} (inscrit par {self.inscrit_par.pseudo}) - {self.evenement.nom}"

    # Méthode pour calculer le montant total
    def calculer_montant_total(self):
        montant = Decimal('0.0')  # Initialiser avec Decimal

        # Ajouter le prix freelance si l'utilisateur est freelance
        if self.utilisateur and self.utilisateur.userprofile.role == 'freelance':
            montant += Decimal(self.evenement.prix_freelance or 0.0)

        # Ajouter le prix du repas
        if self.repas:
            montant += Decimal(self.evenement.prix_repas or 0.0)

        # Ajouter le prix de la location
        if self.location:
            montant += Decimal(self.evenement.prix_location or 0.0)

        return montant




class Lieu(models.Model):
    identifiant = models.SlugField(max_length=50, unique=True)  # Identifiant unique (ex: reignac_1)
    nom_propre = models.CharField(max_length=100)  # Nom propre du terrain (ex: Reignac - Terrain 1)
    note = models.TextField(blank=True, null=True)  # Notes pour le staff
    actif = models.BooleanField(default=True)  # Indique si le terrain est actif ou non
    adresse_postale = models.CharField(max_length=255)  # Adresse complète
    coordonnees_gps = models.CharField(max_length=50)  # Coordonnées GPS (latitude, longitude)
    description_publique = models.TextField(blank=True, null=True)  # Description visible pour le public
    taille = models.FloatField()  # Taille du terrain (en m² par exemple)

    def __str__(self):
        return self.nom_propre
