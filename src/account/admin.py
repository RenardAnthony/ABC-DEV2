from django.contrib import admin
from account.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "pseudo",
        "email",
        "is_active",
    )
    list_per_page = 30
    search_fields = ("email", "pseudo")  # Nécessaire pour l'autocomplétion dans UserBadgeAdmin
