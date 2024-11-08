from django.contrib import admin
from evenement.models import Evenement
from .models import Lieu


@admin.register(Evenement)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "type_evenement",
        "nom",
        "date_heure",
        "lieu",
        "freelance",
        "locations",
        "repas",
    )
    list_per_page = 30

@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ['nom_propre', 'adresse_postale', 'actif']
    search_fields = ['nom_propre', 'adresse_postale']
    list_filter = ['actif']