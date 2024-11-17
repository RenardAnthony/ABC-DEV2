from django.core.management.base import BaseCommand
from badges.models import Badge

class Command(BaseCommand):
    help = 'Crée les badges par défaut pour le site en production'

    def handle(self, *args, **kwargs):
        # Liste des badges à créer
        badges_data = [
            {"name": "Badge des 2 ans", "description": "Attribué aux membres ayant 2 ans d'ancienneté", "rarity": 2},
            {"name": "Le couteau 2024", "description": "Attribué au joueur ayant le plus d'éliminations au couteau en 2024", "rarity": 3},
            {"name": "Frizer", "description": "Attribué au joueur ayant réalisé le plus de freezes en 2024", "rarity": 3},
            {"name": "Badge du Fondateur", "description": "Attribué aux membres fondateurs de l'association", "rarity": 5},
            {"name": "Badge Participation", "description": "Attribué pour participation à un événement spécial", "rarity": 1},
        ]

        for badge_data in badges_data:
            # Crée le badge s'il n'existe pas déjà
            badge, created = Badge.objects.get_or_create(
                name=badge_data["name"],
                defaults={
                    "description": badge_data["description"],
                    "rarity": badge_data["rarity"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Badge "{badge.name}" créé avec succès'))
            else:
                self.stdout.write(self.style.WARNING(f'Badge "{badge.name}" existe déjà'))

        self.stdout.write(self.style.SUCCESS('Tous les badges par défaut ont été créés ou vérifiés avec succès.'))

#python manage.py create_badges

