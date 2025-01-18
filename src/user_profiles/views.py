from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, RolePermission
from .forms import UserProfileForm
from PIL import Image
import os
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

def crop_center(image, size):
    """Crop the image to the center with a square size."""
    width, height = image.size
    new_width, new_height = size, size

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    return image.crop((left, top, right, bottom))

def update_user_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Gestion de l'ancienne image
            old_avatar_path = None
            if user_profile.avatar and user_profile.avatar.name != 'clients/avatars/profil_default.png':
                old_avatar_path = os.path.join(settings.MEDIA_ROOT, user_profile.avatar.name)

            # Sauvegarder le profil utilisateur (et donc l'avatar)
            form.save()

            # Si un nouvel avatar a été téléchargé, gérer le redimensionnement et le nommage
            if 'avatar' in request.FILES:
                image = form.cleaned_data['avatar']
                extension = image.name.split('.')[-1]
                new_image_name = f"{request.user.id}.{extension}"

                # Répertoire pour enregistrer l'image
                image_dir = os.path.join(settings.MEDIA_ROOT, 'clients', 'avatars')
                os.makedirs(image_dir, exist_ok=True)

                # Redimensionner et cropper l'image au centre
                img = Image.open(image)
                img = crop_center(img, min(img.size))  # Crop l'image au carré
                img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Redimensionner

                # Sauvegarder l'image recadrée
                img_path = os.path.join(image_dir, new_image_name)
                img.save(img_path)

                # Mettre à jour l'avatar de l'utilisateur avec le nouveau chemin
                user_profile.avatar = os.path.join('clients', 'avatars', new_image_name)
                user_profile.save()

                # Supprimer l'ancienne image si elle existe
                if old_avatar_path and os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)

            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profile')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profiles/update_profile.html', {'form': form})


@staff_member_required
def populate_role_permissions(request):
    permissions = [
        {"name": "hab_chrony", "denomination": "Habilitation Chrony", "description": "Peut valider les puissances des répliques au chrony."},
        {"name": "hab_payment", "denomination": "Habilitation Validation Paiement", "description": "Peut valider les paiements lors des parties."},
        {"name": "hab_secu", "denomination": "Habilitation Sécurité", "description": "Peut effectuer le briefing sécurité."},
        {"name": "hab_loc", "denomination": "Habilitation Location", "description": "Peut effectuer le briefing des packs de location."},
        {"name": "hab_orga", "denomination": "Habilitation Organisation de Partie", "description": "Peut créer, modifier et supprimer des parties."},
        {"name": "hab_modo", "denomination": "Habilitation Moderation web", "description": "Peut supprimer des message, bannire, valider des comptes sur le site."},
    ]

    for perm in permissions:
        # Crée ou récupère la permission avec les nouveaux champs
        role, created = RolePermission.objects.get_or_create(
            name=perm["name"],
            defaults={
                "denomination": perm["denomination"],
                "description": perm["description"],
            }
        )
        if not created:
            # Si le rôle existe déjà, on peut mettre à jour la description et la dénomination
            role.denomination = perm["denomination"]
            role.description = perm["description"]
            role.save()

    return HttpResponse("Permissions ajoutées ou mises à jour avec succès.")