from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    rarity = models.IntegerField(choices=[(i, f"Rareté {i}") for i in range(1, 6)], default=1)
    image = models.ImageField(upload_to='badges/', default='badges/default.png')  # Image par défaut
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Rareté: {self.rarity})"

class UserBadge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.pseudo} - {self.badge.name}"
