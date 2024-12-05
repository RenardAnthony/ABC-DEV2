from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def mark_as_read(request, pk):
    """
    Supprime une notification lorsqu'elle est marquée comme lue.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()  # Supprime la notification
    return JsonResponse({"success": True})


@login_required
def list_notifications(request):
    """
    Retourne la liste des notifications de l'utilisateur, triées par date de création.
    """
    notifications = request.user.notifications.all().order_by('-created_at')
    data = [
        {
            "id": notif.id,
            "message": notif.message,
            "redirect_url": notif.redirect_url,
            "is_read": notif.is_read,
        }
        for notif in notifications
    ]
    return JsonResponse({"notifications": data})


@login_required
def mark_all_as_read(request):
    """
    Marque toutes les notifications non lues comme lues pour l'utilisateur actuel.
    """
    updated_count = request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({"success": True, "updated_count": updated_count})
