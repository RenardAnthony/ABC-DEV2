from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Badge, UserBadge
from account.models import CustomUser
from .forms import AssignBadgeForm
from django.contrib.admin.views.decorators import staff_member_required

def manage_badges(request):
    user = request.user
    user_badges = list(UserBadge.objects.filter(user=user))

    # Créer une liste de 18 éléments, en remplissant les cases avec des badges ou None
    inventory_size = 18
    filled_user_badges = user_badges[:inventory_size]  # Limite à 18 badges si plus
    badges_for_template = filled_user_badges + [None] * (inventory_size - len(filled_user_badges))

    if request.method == 'POST':
        selected_badges_ids = request.POST.getlist('selected_badges')
        # Désélectionner tous les badges
        UserBadge.objects.filter(user=user).update(is_selected=False)
        # Sélectionner uniquement les trois badges choisis
        UserBadge.objects.filter(id__in=selected_badges_ids).update(is_selected=True)

        # Rediriger l'utilisateur vers sa page de profil
        return redirect(reverse('profile'))

    return render(request, 'badges/manage_badges.html', {'badges_for_template': badges_for_template})
