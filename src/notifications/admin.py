from django.contrib import admin
from .models import Notification
from account.models import CustomUser  # Assurez-vous d'importer votre modèle utilisateur

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')  # Colonnes dans l'admin
    list_filter = ('is_read', 'created_at')  # Filtres latéraux
    search_fields = ('message', 'user__pseudo')  # Barre de recherche
    ordering = ('-created_at',)

    # Ajouter une action pour notifier tous les utilisateurs
    actions = ['create_notification_for_all']

    def create_notification_for_all(self, request, queryset):
        """Créer une notification pour tous les utilisateurs"""
        for notif in queryset:
            users = CustomUser.objects.all()  # Sélectionne tous les utilisateurs
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=notif.message,
                    redirect_url=notif.redirect_url
                )
        self.message_user(request, "Notification créée pour tous les utilisateurs.")
    create_notification_for_all.short_description = "Créer une notification pour tous les utilisateurs"

admin.site.register(Notification, NotificationAdmin)
