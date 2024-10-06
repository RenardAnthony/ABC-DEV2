from django.db import models
from account.models import CustomUser #Dependance a l'application "account" pour gere les utilisateur
from django.conf import settings
from django.urls import reverse

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

    ROLE = [
        ('new', 'Nouveau'),
        ('freelance', 'Freelance'),
        ('member', 'Membre'),
        ('staff', 'Staff'),
        # Ajouter d'autres rôles ici si nécessaire
    ]

    bio_gender = models.CharField(max_length=6, choices=BIO_GENDER)

    choices_gender = models.CharField(max_length=30, choices=CHOICES_GENDER, blank=True)

    blood_group = models.CharField(max_length=7, choices=BLOOD_GROUP)

    role = models.CharField(max_length=10, choices=ROLE, default="new")

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