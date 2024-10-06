from django.contrib import admin
from django.conf import settings
import os
from .models import Gun

@admin.action(description="Supprimer les images non utilisé")
def clear_unused_gun_images(modeladmin, request, queryset):
    gun_image_dir = os.path.join(settings.MEDIA_ROOT, 'clients', 'gun')

    # Récupérer la liste des images de répliques utilisées
    used_gun_images = set(Gun.objects.exclude(photo='').values_list('photo', flat=True))

    for image in os.listdir(gun_image_dir):
        image_path = os.path.join('clients', 'gun', image)
        if image_path not in used_gun_images:
            try:
                os.remove(os.path.join(gun_image_dir, image))
            except Exception as e:
                modeladmin.message_user(request, f"Error removing {image}: {e}")

    modeladmin.message_user(request, "Unused gun images cleared successfully.")

@admin.register(Gun)
class GunAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "name",
        "replica_type",
        "joule",
        "last_joule_update",
    )
    list_per_page = 30
    actions = [clear_unused_gun_images]
