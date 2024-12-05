from django.db import models
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
from evenement.models import Evenement  # Importer le modèle Evenement

from django.db.models.signals import post_save
from django.dispatch import receiver



class ChatRoom(models.Model):
    evenement = models.OneToOneField(
        Evenement, on_delete=models.CASCADE, related_name='chat_room', null=True, blank=True
    )
    name = models.CharField(max_length=255)
    is_general = models.BooleanField(default=False)  # True pour le chat général
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    original_content = models.TextField(blank=True, null=True)  # Conserver les versions éditées
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.pseudo}: {self.content[:50]}"

@receiver(post_save, sender=Evenement)
def create_chat_room_for_event(sender, instance, created, **kwargs):
    if created:
        ChatRoom.objects.create(evenement=instance, name=f"Chat for {instance.nom}")