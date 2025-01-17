from django.db import models
from account.models import CustomUser #Dependance a l'application "account" pour gere les utilisateur
from django.conf import settings
from django.urls import reverse



class RolePermission(models.Model):
    """
    Modèle pour les rôle spécifiques avec des permissions. ca ne remplace pas les "role" et
    permet de donner des droit a des utilisateur sans leur donnée un acces staff.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    denomination = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    BIO_GENDER = [
        ('male', 'Homme'),
        ('female', 'Femme'),
    ]

    CHOICES_GENDER = [
        ('female', 'Femme'),
        ('male', 'Homme'),
        ('non_binary', 'Non binaire'),
        ('other', 'Autre'),
        ('not_to_say', 'Je préfère ne pas répondre'),
    ]

    BLOOD_GROUP = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('unknown', 'Inconnu'),
    ]

    ROLE = [ #Ici c'est uniquement le role primaire de notre utilisateur. pour les role de permission c'est dans ROLE_PERM
        ('new', 'Nouveau'),
        ('freelance', 'Freelance'),
        ('member', 'Membre'),
        ('staff', 'Staff'),
    ]

    role = models.CharField(max_length=10, choices=ROLE, default="new")

    role_permissions = models.ManyToManyField(RolePermission, blank=True, related_name="users")

    bio_gender = models.CharField(max_length=6, choices=BIO_GENDER)

    choices_gender = models.CharField(max_length=30, choices=CHOICES_GENDER, blank=True)

    blood_group = models.CharField(max_length=7, choices=BLOOD_GROUP)

    avatar = models.ImageField(upload_to='clients/avatars', default='../static/images/profil_default.png')

    bio = models.CharField(max_length=255, blank=True)

    nom = models.CharField(max_length=30, blank=True)

    prenom = models.CharField(max_length=30, blank=True)

    tel = models.CharField(max_length=10, blank=True)

    adresse = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.pseudo} Profile'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.user.id})

    def has_permission(self, permission_name):
        return self.role_permissions.filter(name=permission_name).exists()