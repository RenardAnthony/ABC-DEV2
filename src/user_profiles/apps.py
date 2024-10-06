from django.apps import AppConfig

class UserProfilesConfig(AppConfig):
    name = 'user_profiles'

    def ready(self):
        import user_profiles.signals  # Assurez-vous que 'user_profiles' est le nom correct de l'application
