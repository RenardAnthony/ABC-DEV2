from django.contrib import admin
from django.conf import settings
import os
from .models import UserProfile, RolePermission

@admin.action(description="Supprimer les images non utilisées")
def clear_unused_avatars(modeladmin, request, queryset):
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'clients', 'avatars')
    default_avatar = 'clients/avatars/profil_default.png'

    # Récupérer la liste des avatars utilisés avec leurs chemins relatifs
    used_avatars = set(UserProfile.objects.exclude(avatar='').values_list('avatar', flat=True))

    for image in os.listdir(avatar_dir):
        image_path = os.path.join('clients', 'avatars', image)
        if image_path not in used_avatars and image_path != default_avatar:
            try:
                os.remove(os.path.join(avatar_dir, image))
            except Exception as e:
                modeladmin.message_user(request, f"Erreur lors de la suppression de {image} : {e}")

    modeladmin.message_user(request, "Images non utilisées supprimées avec succès.")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "prenom",
        "nom",
        "bio_gender",
        "choices_gender",
        "blood_group",
        "role",
        "tel",
        "adresse",
        "get_permissions",
    )
    list_per_page = 30
    list_filter = ('role',)
    actions = [clear_unused_avatars]

    def get_permissions(self, obj):
        return ", ".join([perm.denomination for perm in obj.role_permissions.all()])

    get_permissions.short_description = "Permissions"

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('denomination', 'name', 'description')
    search_fields = ('name', 'denomination')
