from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from user_profiles.models import UserProfile
from .forms import EvenementForm, LieuForm
from .models import Lieu
from django.template.defaultfilters import register
from collections import Counter
from .models import Evenement, Inscription, Gun, CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from notifications.utils import CreateNotification

from datetime import datetime

def evenement_create_or_update(request, pk=None):

    # Verifier permission de l'utilisateur
    user_profile = request.user.userprofile
    if user_profile.role != "staff" and not user_profile.has_permission("hab_orga"):
        return HttpResponseForbidden("Vous n'avez pas la permission de crée ou modifier des partie")
    ################


    evenement = get_object_or_404(Evenement, pk=pk) if pk else None

    if request.method == 'POST':
        print("Données POST reçues :", request.POST)  # Ajouté pour déboguer
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            evenement = form.save(commit=False)

            process_type_evenement(request, evenement)
            process_repliques(evenement, request)
            process_options(request, evenement)
            process_prix(request, evenement)
            process_adresse(request, evenement)

            print("Adresse après process_adresse :", evenement.adresse)  # Ajouté pour vérifier l'adresse

            evenement.save()

            # Si c'est une création (pas une mise à jour), notifier les utilisateurs
            if not pk:  # Si pk est None, c'est une création
                notify_users_about_event(evenement)

            messages.success(request, "Événement mis à jour avec succès." if pk else "Événement créé avec succès.")
            return redirect('evenement_list')
        else:
            print("Formulaire non valide :", form.errors)  # Ajouté pour déboguer les erreurs de validation
    else:
        form = EvenementForm(instance=evenement)
        prepare_context(evenement, form)

    return render(request, 'evenement/evenement_form.html', prepare_context(evenement, form))

def process_type_evenement(request, evenement):
    """Enregistre le type d'événement (Evenement ou Partie)"""
    type_evenement_checkbox = request.POST.get('type_evenement_toggle')
    evenement.type_evenement = 'Evenement' if type_evenement_checkbox == 'on' else 'Partie'

def process_repliques(evenement, request):
    """Récupère et enregistre les répliques sélectionnées et leurs limites"""
    selected_repliques = request.POST.get('type_replique_autorisee_hidden', '')
    selected_repliques = selected_repliques.split(',') if selected_repliques else []
    evenement.type_replique_autorisee = selected_repliques

    evenement.limite_dmr = request.POST.get('limite_DMR', 0) if 'DMR' in selected_repliques else 0
    evenement.limite_aeg = request.POST.get('limite_AEG', 0) if 'AEG' in selected_repliques else 0
    evenement.limite_smg = request.POST.get('limite_SMG', 0) if 'SMG' in selected_repliques else 0
    evenement.limite_pa = request.POST.get('limite_PA', 0) if 'PA' in selected_repliques else 0
    evenement.limite_pompe = request.POST.get('limite_POMPE', 0) if 'POMPE' in selected_repliques else 0
    evenement.limite_mg = request.POST.get('limite_MG', 0) if 'MG' in selected_repliques else 0
    evenement.limite_autre = request.POST.get('limite_AUTRE', 0) if 'AUTRE' in selected_repliques else 0

def process_options(request, evenement):
    """Enregistre les options (freelance, location, repas)"""
    evenement.freelance = 'freelance' in request.POST
    evenement.locations = 'locations' in request.POST
    evenement.repas = request.POST.get('repas', False)

def process_prix(request, evenement):
    """Gestion des prix avec validation pour les champs vides"""
    def to_float(value):
        try:
            return float(value) if value else 0.0
        except ValueError:
            return 0.0

    evenement.prix_freelance = to_float(request.POST.get('prix_freelance', 0))
    evenement.prix_location = to_float(request.POST.get('prix_location', 0))
    evenement.prix_repas = to_float(request.POST.get('prix_repas', 0))

def process_adresse(request, evenement):
    """Enregistre l'adresse en fonction du lieu sélectionné"""
    lieu_id = request.POST.get('lieu')
    try:
        lieu = Lieu.objects.get(pk=lieu_id)
        evenement.adresse = lieu.adresse_postale or lieu.coordonnees_gps
        evenement.lieu = lieu
        evenement.adresse_autre = None
        print("Adresse récupérée du lieu :", evenement.adresse)
    except Lieu.DoesNotExist:
        evenement.adresse = ''
        evenement.lieu = None
        evenement.adresse_autre = None
        print("Aucune adresse trouvée pour le lieu sélectionné")

def prepare_context(evenement, form):
    """Prépare le contexte pour le rendu de la vue"""
    # Convertir la date au format attendu par le champ datetime-local si l'événement existe
    if evenement and evenement.date_heure:
        form.initial['date_heure'] = evenement.date_heure.strftime('%Y-%m-%dT%H:%M')

    return {
        'form': form,
        'limite_dmr': evenement.limite_dmr if evenement else 0,
        'limite_aeg': evenement.limite_aeg if evenement else 0,
        'limite_smg': evenement.limite_smg if evenement else 0,
        'limite_pa': evenement.limite_pa if evenement else 0,
        'limite_pompe': evenement.limite_pompe if evenement else 0,
        'limite_mg': evenement.limite_mg if evenement else 0,
        'limite_autre': evenement.limite_autre if evenement else 0,
        'freelance': evenement.freelance if evenement else False,
        'locations': evenement.locations if evenement else False,
        'repas': evenement.repas if evenement else False,
        'prix_freelance': evenement.prix_freelance if evenement else 0,
        'prix_location': evenement.prix_location if evenement else 0,
        'prix_repas': evenement.prix_repas if evenement else 0,
        'type_evenement': evenement.type_evenement if evenement else 'Partie',
    }


def evenement_delete(request, pk):

    # Verifier permission de l'utilisateur
    user_profile = request.user.userprofile
    if user_profile.role != "staff" and not user_profile.has_permission("hab_orga"):
        return HttpResponseForbidden("Vous n'avez pas la permission de crée ou modifier des partie")
    ################

    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == "POST":
        evenement.delete()
        return redirect('evenement_list')
    return render(request, 'evenement/evenement_confirm_delete.html', {'evenement': evenement})


def evenement_list(request):

    today = timezone.now()

    annee_actuelle = today.year
    debut_annee = datetime(annee_actuelle, 1, 1, tzinfo=timezone.utc)
    fin_annee = datetime(annee_actuelle, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    evenements_futurs = Evenement.objects.filter(date_heure__gte=today).order_by('date_heure').prefetch_related('inscription_set')
    evenements_passes = Evenement.objects.filter(date_heure__lt=today).order_by('-date_heure').prefetch_related('inscription_set')
    evenements = list(evenements_futurs) + list(evenements_passes)

    evenements_details = []

    # Vérification des permissions pour le bouton de création
    can_create_event = False
    if request.user:
        if request.user.is_staff:
            can_create_event = True
        else :
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_orga"): # or user_profile.has_permission("hab_event_manager"):...
                        can_create_event = True
            except UserProfile.DoesNotExist:
                pass
    #######################


    for evenement in evenements:

        is_event_in_future = evenement.date_heure >= today
        nombre_participants = evenement.inscription_set.count()
        places_restantes = evenement.nb_joueurs_max - nombre_participants

        # Vérifier si l'utilisateur est connecté et s'il est inscrit
        if isinstance(request.user, AnonymousUser):
            utilisateur_inscrit = False  # Utilisateur anonyme, pas inscrit
        else:
            utilisateur_inscrit = evenement.inscription_set.filter(utilisateur=request.user).exists()

        evenements_details.append({
            'evenement': evenement,
            'nombre_participants': nombre_participants,
            'places_restantes': places_restantes,
            'utilisateur_inscrit': utilisateur_inscrit,
            'is_event_in_future': is_event_in_future,
            'today': today,
        })

    return render(request, 'evenement/evenement_list.html', {
        'evenements_details': evenements_details,
        'can_create_event': can_create_event,
    })


def evenement_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    inscriptions = evenement.inscription_set.all()

    chat_room = evenement.chat_room  # Récupérer la salle de discussion associée
    messages = chat_room.messages.filter(is_deleted=False).order_by('-created_at') if chat_room else [] # Messages les plus récents en premier

    today = timezone.now()

    # Récupérer le nombre maximum de joueurs
    nombre_max_joueurs = evenement.nb_joueurs_max

    # Compter combien de répliques sont utilisées par type
    count_repliques = Counter()
    for inscription in inscriptions:
        for replique in inscription.repliques.all():
            count_repliques[replique.replica_type] += 1

    # Vérifier si une réplique est limitée (moins de slots que le nombre de joueurs max)
    limited_replicas = {
        'AEG': evenement.limite_aeg < nombre_max_joueurs,
        'SMG': evenement.limite_smg < nombre_max_joueurs,
        'PA': evenement.limite_pa < nombre_max_joueurs,
        'POMPE': evenement.limite_pompe < nombre_max_joueurs,
        'MG': evenement.limite_mg < nombre_max_joueurs,
        'DMR': evenement.limite_dmr < nombre_max_joueurs,
        'AUTRE': evenement.limite_autre < nombre_max_joueurs,
    }

    # Créer une liste de participants avec leurs répliques ou options de location
    participants = []
    for inscription in inscriptions:
        joueur = inscription.utilisateur.pseudo if inscription.utilisateur else inscription.nom_ami
        repliques = list(inscription.repliques.all())

        # Cas où l'ami apporte ses propres répliques
        repliques_ami = inscription.amis_repliques.split(",") if inscription.amis_repliques else []

        replique_affichee = None

        # Si l'ami utilise un pack de location
        if inscription.location:
            replique_affichee = "Location"
        elif inscription.replique_ami:
            replique_affichee = f"{inscription.replique_ami.replica_type}"
        elif repliques_ami:
            repliques_limited_ami = [r for r in repliques_ami if limited_replicas.get(r, False)]
            repliques_unlimited_ami = [r for r in repliques_ami if not limited_replicas.get(r, False)]

            if repliques_limited_ami:
                replique_affichee = ', '.join(repliques_limited_ami)
            else:
                replique_affichee = ', '.join(repliques_unlimited_ami)
        elif repliques:
            repliques_limited = [r.replica_type for r in repliques if limited_replicas.get(r.replica_type, False)]
            repliques_unlimited = [r.replica_type for r in repliques if not limited_replicas.get(r.replica_type, False)]

            if repliques_limited:
                replique_affichee = ', '.join(repliques_limited)
            else:
                replique_affichee = ', '.join(repliques_unlimited)

        participants.append({
            'joueur': joueur,
            'repliques': replique_affichee if replique_affichee else 'Aucune réplique sélectionnée',
            'inscription': inscription,
        })

    # Calculer les places restantes
    places_restantes = nombre_max_joueurs - evenement.inscription_set.count()

    # Vérifier si l'utilisateur est inscrit à l'événement
    is_inscrit = False
    if request.user.is_authenticated:
        is_inscrit = Inscription.objects.filter(evenement=evenement, utilisateur=request.user).exists()

    # Récupérer le rôle de l'utilisateur si connecté
    user_role = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile:
            user_role = user_profile.role

    # Vérification des permissions
    can_manage_event = False
    if request.user:
        if request.user.is_staff:
            can_manage_event = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_orga") or user_profile.has_permission("hab_event_manager"):
                    can_manage_event = True
            except UserProfile.DoesNotExist:
                pass

    can_show_conta = False
    if request.user:
        if request.user.is_staff:
            can_show_conta = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_orga") or user_profile.has_permission("hab_chrony") or user_profile.has_permission("hab_payment"):
                    can_show_conta = True
            except UserProfile.DoesNotExist:
                pass

    can_show_manage = False
    if request.user:
        if request.user.is_staff:
            can_show_manage = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_orga"):
                    can_show_manage = True
            except UserProfile.DoesNotExist:
                pass

    can_delete_message = False
    if request.user:
        if request.user.is_staff:
            can_delete_message = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_modo"):
                    can_delete_message = True
            except UserProfile.DoesNotExist:
                pass

    #######################


    return render(request, 'evenement/evenement_detail.html', {
        'evenement': evenement,
        'participants': participants,
        'count_repliques': count_repliques,
        'places_restantes': places_restantes,
        'is_inscrit': is_inscrit,
        'user_role': user_role,
        'today': today,
        'messages': messages,
        'chat_room': chat_room,
        'can_manage_event': can_manage_event,
        'can_show_conta': can_show_conta,
        'can_show_manage': can_show_manage,
        'can_delete_message': can_delete_message,
    })




@login_required
def inscription_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    replique_utilisateur = Gun.objects.filter(owner=request.user)

    # Get current counts of replica types already registered (places prises)
    aeg_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="AEG").count()
    smg_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="SMG").count()
    pa_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="PA").count()
    pompe_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="POMPE").count()
    mg_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="MG").count()
    dmr_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="DMR").count()
    autre_inscrits = Inscription.objects.filter(evenement=evenement, repliques__replica_type="AUTRE").count()

    # Calculate available slots and total slots
    slots_info = {
        'AEG': {'total': evenement.limite_aeg, 'pris': aeg_inscrits},
        'SMG': {'total': evenement.limite_smg, 'pris': smg_inscrits},
        'PA': {'total': evenement.limite_pa, 'pris': pa_inscrits},
        'POMPE': {'total': evenement.limite_pompe, 'pris': pompe_inscrits},
        'MG': {'total': evenement.limite_mg, 'pris': mg_inscrits},
        'DMR': {'total': evenement.limite_dmr, 'pris': dmr_inscrits},
        'AUTRE': {'total': evenement.limite_autre, 'pris': autre_inscrits},
    }

    @register.filter
    def get_slots(value, arg):
        return value.get(arg, {'total': 0, 'pris': 0})

    if request.method == 'POST':
        repas = 'repas' in request.POST
        location = 'location' in request.POST
        besoin_covoiturage = 'besoin_covoiturage' in request.POST
        offre_covoiturage = 'offre_covoiturage' in request.POST
        accepte_regles = 'accepte_regles' in request.POST
        replique_ids = request.POST.getlist('replique_ids')

        if not accepte_regles:
            messages.error(request, "Vous devez accepter les règles pour vous inscrire.")
            return redirect('inscription_evenement', evenement_id=evenement_id)

        # Continue with the registration as usual
        inscription, created = Inscription.objects.get_or_create(
            utilisateur=request.user,
            evenement=evenement,
            defaults={
                'repas': repas,
                'location': location,
                'besoin_covoiturage': besoin_covoiturage,
                'offre_covoiturage': offre_covoiturage,
                'accepte_regles': accepte_regles,
                'inscrit_par': request.user,
            }
        )

        if replique_ids:
            repliques = Gun.objects.filter(id__in=replique_ids)
            inscription.repliques.set(repliques)

            # Calculer et sauvegarder le montant total
            inscription.montant_total = inscription.calculer_montant_total()
            inscription.save()


        if not created:
            messages.info(request, "Vous êtes déjà inscrit à cet événement.")
        else:
            messages.success(request, f"Inscription réussie ! Vous devrez payer {inscription.montant_total:.2f} €.")

        return redirect('evenement_detail', pk=evenement_id)

    return render(request, 'evenement/inscription.html', {
        'evenement': evenement,
        'replique_utilisateur': replique_utilisateur,
        'slots_info': slots_info,  # Pass the slots information to the template
    })

@login_required
def inscription_ami(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    montant_total = evenement.prix_freelance or 0

    # Récupérer les types de répliques autorisées et les informations de slots
    types_repliques_autorisees = evenement.get_type_replique_autorisee()
    slots_info = [
        {
            'type': 'AEG',
            'total': evenement.limite_aeg,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="AEG").count()
        },
        {
            'type': 'SMG',
            'total': evenement.limite_smg,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="SMG").count()
        },
        {
            'type': 'PA',
            'total': evenement.limite_pa,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="PA").count()
        },
        {
            'type': 'POMPE',
            'total': evenement.limite_pompe,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="POMPE").count()
        },
        {
            'type': 'MG',
            'total': evenement.limite_mg,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="MG").count()
        },
        {
            'type': 'DMR',
            'total': evenement.limite_dmr,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="DMR").count()
        },
        {
            'type': 'AUTRE',
            'total': evenement.limite_autre,
            'pris': Inscription.objects.filter(evenement=evenement, repliques__replica_type="AUTRE").count()
        }
    ]

    if request.method == 'POST':
        nom_ami = request.POST.get('nom_ami')
        repas = 'repas' in request.POST
        location = 'location' in request.POST
        besoin_covoiturage = 'besoin_covoiturage' in request.POST
        offre_covoiturage = 'offre_covoiturage' in request.POST
        accepte_regles = 'accepte_regles' in request.POST

        # Vérification des champs obligatoires
        if not nom_ami:
            messages.error(request, "Vous devez entrer le nom de l'ami.")
            return redirect('inscription_ami', evenement_id=evenement_id)

        if not accepte_regles:
            messages.error(request, "Vous devez accepter les règles pour inscrire votre ami.")
            return redirect('inscription_ami', evenement_id=evenement_id)

        # Gestion du choix de réplique
        choix_replique = request.POST.get('replique_choice')
        replique_ami = None
        amis_repliques = ''

        if choix_replique == 'pack_location':
            location = True
        elif choix_replique == 'pret_replique':
            replique_ami_id = request.POST.get('replique_ami')
            if replique_ami_id:
                try:
                    replique_ami = Gun.objects.get(id=replique_ami_id)
                except Gun.DoesNotExist:
                    messages.error(request, "La réplique sélectionnée n'existe pas.")
                    return redirect('inscription_ami', evenement_id=evenement_id)
        elif choix_replique == 'ami_replique':
            amis_repliques_ids = request.POST.getlist('amis_repliques')
            if amis_repliques_ids:
                amis_repliques = ','.join(amis_repliques_ids)  # Stocker les types de répliques sélectionnées comme une chaîne de caractères

        # Enregistrement de l'inscription de l'ami
        inscription, created = Inscription.objects.get_or_create(
            evenement=evenement,
            nom_ami=nom_ami,
            defaults={
                'repas': repas,
                'location': location,
                'besoin_covoiturage': besoin_covoiturage,
                'offre_covoiturage': offre_covoiturage,
                'accepte_regles': accepte_regles,
                'inscrit_par': request.user,
                'replique_ami': replique_ami,
                'amis_repliques': amis_repliques  # Stocker les répliques de l'ami comme une chaîne de caractères
            }
        )

        if not created:
            messages.info(request, f"{nom_ami} est déjà inscrit à cet événement.")
        else:
            inscription.montant_total = montant_total + (evenement.prix_repas if repas else 0) + (evenement.prix_location if location else 0)
            inscription.save()
            messages.success(request, f"{nom_ami} a été inscrit avec succès ! Vous devrez payer {montant_total} €.")

        return redirect('evenement_detail', pk=evenement_id)

    # Passer les types de répliques autorisées et les informations des slots au template
    replique_utilisateur = Gun.objects.filter(owner=request.user)
    return render(request, 'evenement/inscription_ami.html', {
        'evenement': evenement,
        'montant_total': montant_total,
        'replique_utilisateur': replique_utilisateur,
        'types_repliques_autorisees': types_repliques_autorisees,
        'slots_info': slots_info
    })




@login_required
def desinscription_evenement(request, evenement_id):
    evenement = get_object_or_404(Evenement, id=evenement_id)
    inscription = Inscription.objects.filter(utilisateur=request.user, evenement=evenement).first()

    if inscription:
        # Supprimer les inscriptions des amis que cet utilisateur a inscrits
        Inscription.objects.filter(inscrit_par=request.user, evenement=evenement).delete()

        # Supprimer l'inscription de l'utilisateur
        inscription.delete()
        messages.success(request, "Vous vous êtes désinscrit avec succès, ainsi que tous les amis que vous aviez inscrits.")
    else:
        messages.error(request, "Vous n'êtes pas inscrit à cet événement.")

    return redirect('evenement_detail', pk=evenement.id)



# Comptabilité de l'événement
def comptabilite_evenement(request, pk):


    # Verifier permission de l'utilisateur
    user_profile = request.user.userprofile
    if user_profile.role != "staff" and not (
            user_profile.has_permission("hab_orga") or
            user_profile.has_permission("hab_chrony") or
            user_profile.has_permission("hab_payment")
    ):
        return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")
    ################


    evenement = get_object_or_404(Evenement, pk=pk)
    inscriptions = evenement.inscription_set.all()

    participants = []
    total_depenses = 0
    total_repas = 0
    total_locations = 0
    total_freelance = 0
    total_membre = 0
    repliques_par_categorie = {
        'AEG': 0,
        'SMG': 0,
        'PA': 0,
        'POMPE': 0,
        'MG': 0,
        'DMR': 0,
        'AUTRE': 0
    }

    for inscription in inscriptions:
        # On calcule le montant total comme précédemment
        depense = inscription.montant_total

        # Si l'utilisateur est un ami, on ajoute l'inviteur
        if inscription.nom_ami:
            pseudo = f"{inscription.nom_ami} ({inscription.inscrit_par.pseudo})"
            total_freelance += 1  # Les amis sont toujours considérés comme freelances
        else:
            pseudo = inscription.utilisateur.pseudo if inscription.utilisateur else 'Utilisateur inconnu'
            if inscription.utilisateur and inscription.utilisateur.userprofile.role == 'freelance':
                total_freelance += 1
            else:
                total_membre += 1

        # On compte les repas et les locations
        if inscription.repas:
            total_repas += 1
        if inscription.location:
            total_locations += 1

        # On compte les répliques par catégorie
        for replique in inscription.repliques.all():
            if replique.replica_type in repliques_par_categorie:
                repliques_par_categorie[replique.replica_type] += 1

        participants.append({
            'inscription_id': inscription.id,
            'pseudo': pseudo,
            'depense': depense,
            'paiement_valide': inscription.paiement_valide,
            'chrony_valide': inscription.chrony_valide,
        })
        total_depenses += depense

    # Vérifier si l'utilisateur est inscrit à l'événement
    is_inscrit = False
    if request.user.is_authenticated:
        is_inscrit = Inscription.objects.filter(evenement=evenement, utilisateur=request.user).exists()

    # Récupérer le rôle de l'utilisateur si connecté
    user_role = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile:
            user_role = user_profile.role

    # Vérification des permissions
    can_show_monney = False
    if request.user:
        if request.user.is_staff:
            can_show_monney = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_orga") or user_profile.has_permission("hab_payment"):
                    can_show_monney = True
            except UserProfile.DoesNotExist:
                pass


    #######################


    return render(request, 'evenement/comptabilite.html', {
        'evenement': evenement,
        'participants': participants,
        'total_depenses': total_depenses,
        'total_repas': total_repas,
        'total_locations': total_locations,
        'total_freelance': total_freelance,
        'total_membre': total_membre,
        'repliques_par_categorie': repliques_par_categorie,
        'can_show_monney': can_show_monney,
    })








def gestion_participant(request, evenement_id, inscription_id):

    # Verifier permission de l'utilisateur
    user_profile = request.user.userprofile
    if user_profile.role != "staff" and not (
            user_profile.has_permission("hab_orga") or
            user_profile.has_permission("hab_chrony") or
            user_profile.has_permission("hab_payment")
    ):
        return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")
    ################

    evenement = get_object_or_404(Evenement, id=evenement_id)
    inscription = get_object_or_404(Inscription, id=inscription_id)

    # Initialiser la dépense
    depense = inscription.montant_total
    depense_details = []

    # Ajouter les détails du prix pour l'affichage
    if inscription.utilisateur and inscription.utilisateur.userprofile.role == 'freelance':
        depense_details.append(f"{evenement.prix_freelance} € pour la PAF")

    if inscription.repas:
        depense_details.append(f"{evenement.prix_repas} € pour le repas")

    if inscription.location:
        depense_details.append(f"{evenement.prix_location} € pour la location")

    # Répliques sélectionnées pour l'événement
    repliques_selectionnees = []
    repliques_non_selectionnees = []
    amis_repliques = []

    if inscription.replique_ami:
        # Cas où l'utilisateur a prêté une réplique à l'ami
        replique = inscription.replique_ami
        status = "OK"
        if replique.replica_type not in evenement.get_type_replique_autorisee():
            status = "Non compatible"
        elif Inscription.objects.filter(evenement=evenement,
                                        repliques__replica_type=replique.replica_type).count() >= evenement.limite_aeg:
            status = "Trop de répliques de ce type"
        elif replique.joule and replique.joule > evenement.puissance_max_joule:
            status = "Puissance trop élevé"
        elif not replique.last_joule_update or replique.last_joule_update < timezone.now() - timezone.timedelta(
                days=60):
            status = "Vérification Obligatoire"

        replique_info = {
            'id': replique.id,
            'nom': replique.name,
            'type': replique.replica_type,
            'joule': replique.joule,
            'status': status,
            'last_joule_update': replique.last_joule_update,
        }
        repliques_selectionnees.append(replique_info)

    elif inscription.amis_repliques:
        # Cas où l'ami utilise sa propre réplique (les types sont stockés sous forme de chaîne de caractères)
        amis_repliques = inscription.amis_repliques.split(',')  # Transforme la chaîne en liste

    elif inscription.location:
        # Cas où l'utilisateur/ami a pris un pack de location
        repliques_selectionnees.append({'type': 'Location'})

    # Gérer les autres répliques de l'utilisateur (si applicable)
    if inscription.utilisateur:
        toutes_repliques = inscription.utilisateur.guns.all()

        for replique in toutes_repliques:
            status = "OK"
            if replique.replica_type not in evenement.get_type_replique_autorisee():
                status = "Non compatible"
            elif replique.joule and replique.joule > evenement.puissance_max_joule:
                status = "Puissance trop élevé"
            elif not replique.last_joule_update or replique.last_joule_update < timezone.now() - timezone.timedelta(
                    days=60):
                status = "Vérification Obligatoire"

            replique_info = {
                'id': replique.id,
                'nom': replique.name,
                'type': replique.replica_type,
                'joule': replique.joule,
                'status': status,
                'last_joule_update': replique.last_joule_update,
            }

            if replique in inscription.repliques.all():
                repliques_selectionnees.append(replique_info)
            else:
                repliques_non_selectionnees.append(replique_info)

    if request.method == 'POST':
        if 'valider_paiement' in request.POST:
            inscription.paiement_valide = True
            inscription.save()
            messages.success(request, "Le paiement a été validé.")
        elif 'valider_chrony' in request.POST:
            inscription.chrony_valide = True
            inscription.save()
            messages.success(request, "Le chrony a été validé.")

        return redirect('gestion_participant', evenement_id=evenement.id, inscription_id=inscription.id)




    # Vérification des permissions
    can_valider_payment = False
    if request.user:
        if request.user.is_staff:
            can_valider_payment = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_payment"):
                    can_valider_payment = True
            except UserProfile.DoesNotExist:
                pass

    can_valider_chrony = False
    if request.user:
        if request.user.is_staff:
            can_valider_chrony = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_chrony"):
                    can_valider_chrony = True
            except UserProfile.DoesNotExist:
                pass



    context = {
        'evenement': evenement,
        'inscription': inscription,
        'depense': depense,
        'depense_details': depense_details,
        'repliques_selectionnees': repliques_selectionnees,
        'repliques_non_selectionnees': repliques_non_selectionnees,
        'amis_repliques': amis_repliques,  # On passe ici la liste des types de répliques apportées par l'ami
        'can_valider_payment': can_valider_payment,
        'can_valider_chrony': can_valider_chrony,
    }
    return render(request, 'evenement/gestion_participant.html', context)

@staff_member_required
def remplir_bdd_lieux(request):
    # Clear les anciens lieux si besoin (facultatif)
    Lieu.objects.all().delete()

    # Création des trois lieux par défaut
    lieux = [
        Lieu(
            identifiant='cezac',
            nom_propre='Cézac',
            note='Notre forest ABC. Elle nous appartient, il faut en faire quelque chose.',
            actif=True,
            adresse_postale='75 Les Grands Prés, 33620 Cézac',
            coordonnees_gps='45.087150, -0.467506',
            description_publique='Notre terrain d\'entrainement.',
            taille=14000
        ),
        Lieu(
            identifiant='reignac_1',
            nom_propre='Reignac - Terrain 1',
            note='Utilisation restreinte les week-ends.',
            actif=True,
            adresse_postale='D136, 33860 Reignac',
            coordonnees_gps='45.234235, -0.560865',
            description_publique='L\'un de nos deux plus gros terrains en forêt',
            taille=116000
        ),
        Lieu(
            identifiant='reignac_2',
            nom_propre='Reignac - Terrain 2',
            note='Utilisation restreinte les week-ends.',
            actif=True,
            adresse_postale='D136, 33860 Reignac',
            coordonnees_gps='45.236535, -0.559615',
            description_publique='L\'un de nos deux plus gros terrains en forêt',
            taille=148000
        )
    ]

    # Enregistrement dans la base de données
    Lieu.objects.bulk_create(lieux)

    # Message de succès
    messages.success(request, "La base de données a été remplie avec 3 lieux par défaut.")

    return redirect('lieu_list')  # Redirection vers la page où tu veux afficher les lieux

@staff_member_required
def lieu_list(request):
    # On récupère tous les lieux
    lieux = Lieu.objects.all()
    return render(request, 'evenement/lieu_list.html', {'lieux': lieux})


@staff_member_required
def lieu_create_view(request):
    if request.method == 'POST':
        form = LieuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lieu créé avec succès.")
            return redirect('evenement_create_or_update')  # Redirige vers la création d'un événement
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier les informations.")
    else:
        form = LieuForm()

    return render(request, 'evenement/lieu_create_form.html', {'form': form})




def notify_users_about_event(event):
    # Récupérer tous les utilisateurs
    users = CustomUser.objects.all()
    CreateNotification("all", f"Un nouveau événement a été créée : {event.nom}", url=f"/evenement/{event.id}/")
