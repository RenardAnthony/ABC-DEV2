from django.contrib import admin
from .models import Badge, UserBadge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'date_created')
    search_fields = ('name', 'description')
    list_filter = ('rarity',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'date_awarded', 'is_selected')
    search_fields = ('user__pseudo', 'badge__name')
    list_filter = ('badge', 'user')
    autocomplete_fields = ['user', 'badge']  # 'user' fonctionne maintenant, car il est enregistré dans 'account/admin.py'
