from notifications.models import Notification
from account.models import CustomUser

def CreateNotification(for_target, msg, url=None):
    """
    Crée une notification pour un ou plusieurs utilisateurs.

    Args:
        for_target (str|list|CustomUser): À qui envoyer la notification.
            - "all" pour tous les utilisateurs.
            - "group_name" pour un groupe spécifique (par exemple, "admin").
            - Pseudo d'un utilisateur spécifique.
            - Liste de pseudos ou utilisateurs.
        msg (str): Le message de la notification.
        url (str, optional): Lien de redirection attaché à la notification. Defaults to None.

    Returns:
        int: Nombre de notifications créées.
    """
    notifications_created = 0

    if for_target == "all":
        users = CustomUser.objects.all()
    elif isinstance(for_target, str) and for_target in ["staff", "freelance", "member"]:
        users = CustomUser.objects.filter(userprofile__role=for_target)
    elif isinstance(for_target, str):  # Pseudo unique
        users = CustomUser.objects.filter(pseudo=for_target)
    elif isinstance(for_target, list):  # Liste de pseudos ou objets CustomUser
        if isinstance(for_target[0], CustomUser):
            users = for_target
        else:
            users = CustomUser.objects.filter(pseudo__in=for_target)
    else:
        return notifications_created  # Aucune correspondance

    # Créer les notifications pour tous les utilisateurs sélectionnés
    for user in users:
        Notification.objects.create(
            user=user,
            message=msg,
            redirect_url=url
        )
        notifications_created += 1

    return notifications_created
