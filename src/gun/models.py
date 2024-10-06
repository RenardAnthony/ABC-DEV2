from django.db import models
from django.conf import settings
from django.utils import timezone

class Gun(models.Model):
    TYPE_CHOICES = [
        ('AEG', 'AEG'),
        ('SMG', 'SMG'),
        ('PA', 'PA'),
        ('POMPE', 'POMPE'),
        ('MG', 'MG'),
        ('DMR', 'DMR'),
        ('AUTRE', 'AUTRE'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guns')
    replica_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    joule = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Champ pour stocker les joules
    date_added = models.DateTimeField(auto_now_add=True)
    last_joule_update = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='clients/gun', null=True, blank=True)

    class Meta:
        verbose_name = "Réplique"
    def save(self, *args, **kwargs):
        if self.pk is not None:  # Check if the object is already in the database
            old_gun = Gun.objects.get(pk=self.pk)
            if self.joule != old_gun.joule:
                self.last_joule_update = timezone.now()
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_joule = self.joule