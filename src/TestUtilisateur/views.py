from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from account.models import CustomUser  # Assurez-vous que le modèle CustomUser est correctement importé
from evenement.models import Evenement  # Assurez-vous que le modèle Evenement est correctement importé

def index(request):
    # Récupérer l'événement le plus proche de la date actuelle
    prochain_evenement = Evenement.objects.filter(date_heure__gte=timezone.now()).order_by('date_heure').first()

    # Compter le nombre total de membres
    total_membres = CustomUser.objects.count()

    # Compter le nombre de parties jouées cette année
    debut_annee = datetime(datetime.now().year, 1, 1)
    parties_jouees = Evenement.objects.filter(date_heure__gte=debut_annee).count()

    context = {
        'prochain_evenement': prochain_evenement,
        'total_membres': total_membres,
        'parties_jouees': parties_jouees,
    }

    return render(request, "index.html", context)



def test(request):
    return render(request, "test.html")

def tools(request):
    return render(request, "tools.html")