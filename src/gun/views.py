from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GunForm
from .models import Gun
from PIL import Image
import os
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.http import JsonResponse

@login_required
def manage_gun(request, pk=None):
    gun = get_object_or_404(Gun, pk=pk, owner=request.user) if pk else None

    if request.method == "POST":
        form = GunForm(request.POST, request.FILES, instance=gun)
        if form.is_valid():
            gun = form.save(commit=False)
            gun.owner = request.user  # Assigne l'utilisateur connecté comme propriétaire

            # Gestion de l'image
            try:
                if 'photo' in request.FILES:
                    image = request.FILES['photo']
                    extension = image.name.split('.')[-1]
                    new_image_name = f"{request.user.id}_{gun.name.replace(' ', '_')}.{extension}"

                    # Répertoire pour enregistrer l'image
                    image_dir = os.path.join(settings.MEDIA_ROOT, 'clients', 'gun')
                    os.makedirs(image_dir, exist_ok=True)

                    # Ouvrir l'image avec Pillow
                    img = Image.open(image)

                    # Dimensions cibles
                    target_width = 300
                    target_height = 180

                    # Calcul du ratio pour redimensionner sans distorsion
                    width_ratio = target_width / img.width
                    height_ratio = target_height / img.height
                    if width_ratio > height_ratio:
                        new_size = (target_width, int(img.height * width_ratio))
                    else:
                        new_size = (int(img.width * height_ratio), target_height)

                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                    # Centre et recadre l'image pour qu'elle soit exactement de la taille cible
                    left = (img.width - target_width) / 2
                    top = (img.height - target_height) / 2
                    right = (img.width + target_width) / 2
                    bottom = (img.height + target_height) / 2
                    img = img.crop((left, top, right, bottom))

                    # Enregistrer l'image redimensionnée
                    img_path = os.path.join(image_dir, new_image_name)
                    img.save(img_path)

                    # Supprimer l'ancienne image si elle existe
                    if gun.photo and os.path.exists(os.path.join(settings.MEDIA_ROOT, gun.photo.name)):
                        os.remove(os.path.join(settings.MEDIA_ROOT, gun.photo.name))

                    # Mettre à jour le chemin de l'image dans le modèle
                    gun.photo = os.path.join('clients', 'gun', new_image_name)

                gun.save()
                messages.success(request, "Réplique enregistrée avec succès.")
                return redirect('profile')

            except Exception as e:
                # Ajoute un message d'erreur en cas de problème
                messages.error(request, f"Erreur lors du traitement de l'image : {str(e)}")
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier les données.")
    else:
        form = GunForm(instance=gun)

    return render(request, 'gun/gun_form.html', {'form': form, 'gun': gun})


@login_required
def delete_gun(request, pk):
    gun = get_object_or_404(Gun, pk=pk, owner=request.user)
    if request.method == "POST":
        # Supprimer l'image associée si elle existe
        if gun.photo and os.path.exists(os.path.join(settings.MEDIA_ROOT, gun.photo.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, gun.photo.path))

        gun.delete()
        messages.success(request, "Réplique supprimée avec succès.")
        return redirect('profile')
    return render(request, 'gun/gun_confirm_delete.html', {'gun': gun})


@staff_member_required
def verifier_replique(request, replique_id):
    replique = get_object_or_404(Gun, id=replique_id)

    evenement_id = request.GET.get('evenement_id')
    inscription_id = request.GET.get('inscription_id')

    puissance_joules = None  # Variable pour stocker la puissance en joules

    if request.method == 'POST':
        try:
            grammage_bille = float(request.POST.get('grammage_bille').replace(',', '.'))
            fps_mesures = float(request.POST.get('fps').replace(',', '.'))

            # Calcul de la puissance en joules
            puissance_joules = (fps_mesures ** 2) * grammage_bille / 2000
            puissance_joules = puissance_joules / 10
            puissance_joules = round(puissance_joules, 2)

            # Mettez à jour les joules et la date de dernière vérification
            replique.joule = puissance_joules
            replique.last_joule_update = timezone.now()
            replique.save()

            messages.success(request, f"Puissance en joules enregistrée : {puissance_joules:.2f} J")

            # Redirection vers la page de l'événement après validation
            return redirect('gestion_participant', evenement_id=evenement_id, inscription_id=inscription_id)

        except ValueError:
            messages.error(request, "Veuillez entrer des valeurs valides.")

    grams_list = [round(0.10 + i * 0.01, 2) for i in range(31)]  # Liste de 0.10 à 0.40

    context = {
        'replique': replique,
        'evenement_id': evenement_id,
        'inscription_id': inscription_id,
        'puissance_joules': puissance_joules,
        'grams_list': grams_list,
        'proprietaire': replique.owner,
    }
    return render(request, 'gun/verifier_replique.html', context)

@staff_member_required
def calcul_puissance(request):
    puissance_joules = None

    if request.method == 'POST':
        try:
            # Récupération des données utilisateur
            grammage_bille = float(request.POST.get('grammage_bille').replace(',', '.'))
            fps_mesures = float(request.POST.get('fps').replace(',', '.'))

            # Conversion des unités
            masse_kg = grammage_bille / 1000  # Conversion en kilogrammes
            vitesse_ms = fps_mesures * 0.3048  # Conversion FPS en m/s

            # Calcul de la puissance en joules
            puissance_joules = (1 / 2) * masse_kg * (vitesse_ms ** 2)
            puissance_joules = round(puissance_joules, 2)

            return JsonResponse({'success': True, 'puissance_joules': puissance_joules})

        except (ValueError, KeyError):
            return JsonResponse({'success': False, 'message': "Valeurs invalides pour le calcul."})

    return render(request, 'gun/calcul_puissance.html', {'puissance_joules': puissance_joules})