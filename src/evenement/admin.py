from django.contrib import admin
from evenement.models import Evenement



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