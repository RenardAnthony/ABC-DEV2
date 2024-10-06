from django.contrib import admin
import os
from django.conf import settings

# Importation des modèles avec le chemin complet
from user_profiles.models import UserProfile
from gun.models import Gun



@admin.action(description="Clear unused images")
def clear_unused_images(modeladmin, request, queryset):
    avatars_dir = os.path.join(settings.MEDIA_ROOT, 'clients', 'avatars')
    gun_dir = os.path.join(settings.MEDIA_ROOT, 'clients', 'gun')

    used_avatars = set(UserProfile.objects.exclude(avatar='clients/avatars/profil_default.png').values_list('avatar', flat=True))
    used_gun_photos = set(Gun.objects.exclude(photo='').values_list('photo', flat=True))

    def clear_images(directory, used_images):
        for image in os.listdir(directory):
            image_path = os.path.join('clients', directory.split('/')[-1], image)
            if image_path not in used_images:
                os.remove(os.path.join(directory, image))

    clear_images(avatars_dir, used_avatars)
    clear_images(gun_dir, used_gun_photos)

    modeladmin.message_user(request, "Unused images cleared successfully.")

class UserProfileAdmin(admin.ModelAdmin):
    actions = [clear_unused_images]

class GunAdmin(admin.ModelAdmin):
    actions = [clear_unused_images]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Gun, GunAdmin)