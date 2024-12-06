import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Message, ChatRoom


@login_required
def send_message(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    content = request.POST.get('content')

    if content:
        Message.objects.create(room=chat_room, user=request.user, content=content)

    return redirect('evenement_detail', pk=chat_room.evenement.id)


@login_required
def edit_message(request, message_id):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    message = get_object_or_404(Message, id=message_id)

    if request.user != message.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

    try:
        data = json.loads(request.body)
        new_content = data.get('content', '')

        if not new_content.strip():
            return JsonResponse({'success': False, 'error': 'Message content cannot be empty'}, status=400)

        # Mettre à jour le message
        message.original_content = message.content  # Conserver l'ancienne version
        message.content = new_content
        message.save()

        return JsonResponse({'success': True, 'updated_content': message.content})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def delete_message(request, message_id):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    message = get_object_or_404(Message, id=message_id)

    if request.user != message.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

    # Marquer le message comme supprimé
    message.is_deleted = True
    message.save()

    return JsonResponse({'success': True})
