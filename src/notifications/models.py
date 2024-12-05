from datetime import timezone

from django.db import models
from account.models import CustomUser
from django.urls import reverse

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('success', 'Succès'),
        ('alert', 'Alerte'),
    ]

    user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    redirect_url = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=1)  # Priorité : 1 (basse), 2 (moyenne), 3 (haute)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"Notification for {self.user.pseudo}: {self.message}"

    def get_redirect_url(self):
        """Retourne l'URL de redirection ou une valeur par défaut."""
        return self.redirect_url or reverse('some_default_view')

    def mark_as_read(self):
        """Marque la notification comme lue."""
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
