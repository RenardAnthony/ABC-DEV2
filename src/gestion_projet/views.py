from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from datetime import timedelta

from .models import Tag, Task, BugReport, ChatMessage, ActivityLog, Comment, Notification
from .forms import TaskForm, BugReportForm, BugResolutionForm



def format_timestamp(timestamp):
    # Validation du type
    if not isinstance(timestamp, datetime.datetime):
        return "Invalid timestamp"

    # Gestion des fuseaux horaires
    now = timezone.now()
    if timezone.is_aware(timestamp):
        timestamp = timezone.localtime(timestamp)

    # Comparaisons et formatage
    if timestamp.date() == now.date():
        return f"Aujourd'hui à {timestamp.strftime('%H:%M')}"
    elif timestamp.date() == (now - timedelta(days=1)).date():
        return f"Hier à {timestamp.strftime('%H:%M')}"
    elif timestamp.year == now.year:
        return timestamp.strftime('%d %b à %H:%M')
    else:
        return timestamp.strftime('%d %b %Y à %H:%M')

# views.py
@login_required
def vue_d_ensemble(request):
    # Récupère les tâches et bugs non archivés les plus récents ou les plus prioritaires
    tasks = Task.objects.filter(is_archived=False).order_by('-priority')[:5]
    bugs = BugReport.objects.filter(is_resolved=False).order_by('-priority')[:5]

    # Calcul de la progression générale
    total_task_progress = sum(task.progress for task in Task.objects.filter(is_archived=False))
    total_tasks = Task.objects.filter(is_archived=False).count()
    average_task_completion = (total_task_progress / (total_tasks * 100)) * 100 if total_tasks > 0 else 100

    # Calcul de la pénalité pour les bugs
    remaining_bugs = BugReport.objects.filter(is_resolved=False).count()
    total_bugs = BugReport.objects.count()
    bug_penalty = (remaining_bugs / (total_bugs + 1)) * 50  # Ajustement à 50% de la pénalité si bugs présents

    # Calcul final de la progression générale
    project_progress = int(max(0, min(100, average_task_completion - bug_penalty)))


    # Récupérer les messages récents du chat
    chat_messages = ChatMessage.objects.order_by('timestamp')[:5]

    # Récupérer les actions récentes
    recent_activity = ActivityLog.objects.order_by('timestamp')[:5]

    context = {
        'tasks': tasks,
        'bugs': bugs,
        'project_progress': round(project_progress, 2),
        'chat_messages': chat_messages,
        'recent_activity': recent_activity,
        'total_bugs': remaining_bugs,
        'total_tasks': Task.objects.filter(progress__lt=100, is_archived=False).count(),
    }
    return render(request, 'gestion_projet/vue_d_ensemble.html', context)





# views.py
@login_required
def taches(request):
    priority_filter = request.GET.get('priority')
    task_list = Task.objects.filter(is_archived=False)
    if priority_filter:
        task_list = task_list.filter(priority=priority_filter)
    task_list = task_list.order_by('-priority')

    # Pagination
    paginator = Paginator(task_list, 10)  # Affiche 10 tâches par page
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    context = {'tasks': tasks}
    return render(request, 'gestion_projet/taches.html', context)


@login_required
def bugs(request):
    priority_filter = request.GET.get('priority')
    bug_list = BugReport.objects.filter(is_archived=False)

    if priority_filter:
        bug_list = bug_list.filter(priority=priority_filter)

    # Pagination
    paginator = Paginator(bug_list, 10)  # Affiche 10 bugs par page
    page = request.GET.get('page')
    try:
        bugs = paginator.page(page)
    except PageNotAnInteger:
        bugs = paginator.page(1)
    except EmptyPage:
        bugs = paginator.page(paginator.num_pages)

    context = {'bugs': bugs}
    return render(request, 'gestion_projet/bugs.html', context)


@login_required
def live_chat(request):
    if request.method == "POST":
        message_content = request.POST.get("message")
        if message_content:
            ChatMessage.objects.create(user=request.user, message=message_content)
        return redirect('live_chat')

    chat_messages = ChatMessage.objects.order_by('timestamp')[:50]  # Récupère les 50 derniers messages
    context = {'chat_messages': chat_messages}
    return render(request, 'gestion_projet/live_chat.html', context)




@login_required
def statistiques(request):
    total_tasks = Task.objects.count()
    total_bugs = BugReport.objects.count()
    completed_tasks = Task.objects.filter(progress=100).count()

    # Statistiques pour les graphiques
    task_priorities = Task.objects.values('priority').annotate(count=Count('id'))
    bug_priorities = BugReport.objects.values('priority').annotate(count=Count('id'))

    context = {
        'total_tasks': total_tasks,
        'total_bugs': total_bugs,
        'completed_tasks': completed_tasks,
        'task_priorities': task_priorities,
        'bug_priorities': bug_priorities
    }
    return render(request, 'gestion_projet/statistiques.html', context)

@login_required
def initialiser_tags(request):
    # Vérifier s'il y a déjà des tags pour éviter les doublons
    if Tag.objects.exists():
        return HttpResponse("Les tags existent déjà dans la base de données.")

    # Création des tags avec les couleurs spécifiées
    tags = [
        {"name": "Responsive", "color": "#28A745"},  # Vert
        {"name": "Orthographe", "color": "#FFC0CB"},  # Rose
        {"name": "Backend", "color": "#FF0000"},      # Rouge
        {"name": "Frontend", "color": "#7d32dd"}, #Violet
    ]

    # Boucle pour ajouter les tags dans la base de données
    for tag_data in tags:
        Tag.objects.create(name=tag_data["name"], color=tag_data["color"])

    return HttpResponse("Tags initialisés avec succès.")


@login_required
def archiver_tache(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_archived = True
    task.save()
    return redirect('taches')

@login_required
def archiver_bug(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)
    bug.is_archived = True
    bug.save()
    return redirect('bugs')

@login_required
def archive_item(request, item_type, item_id):
    model = Task if item_type == 'task' else BugReport
    item = get_object_or_404(model, id=item_id)
    item.is_archived = True
    item.save()
    return redirect('taches' if item_type == 'task' else 'bugs')


@login_required
def tache_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = Comment.objects.filter(task=task).order_by('-timestamp')
    chat_messages = ChatMessage.objects.filter(task=task).order_by('timestamp')

    if request.method == 'POST':
        message_content = request.POST.get("message")
        if message_content:
            ChatMessage.objects.create(user=request.user, message=message_content, task=task)
        return redirect('tache_detail', task_id=task.id)

    return render(request, 'gestion_projet/tache_detail.html', {
        'task': task,
        'comments': comments,
        'chat_messages': chat_messages,
        'created_by': task.created_by.username if task.created_by else "Utilisateur externe",
        'created_at': task.created_at,
    })


@login_required
def bug_detail(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)
    comments = Comment.objects.filter(bug=bug).order_by('-timestamp')
    chat_messages = ChatMessage.objects.filter(bug=bug).order_by('timestamp')

    if request.method == 'POST':
        message_content = request.POST.get("message")
        if message_content:
            ChatMessage.objects.create(user=request.user, message=message_content, bug=bug)
        return redirect('bug_detail', bug_id=bug.id)

    return render(request, 'gestion_projet/bug_detail.html', {
        'bug': bug,
        'comments': comments,
        'chat_messages': chat_messages,
        'created_by': bug.created_by.username if bug.created_by else "Utilisateur externe",
        'created_at': bug.created_at,
    })


@login_required
def marquer_notifications_comme_lues(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notifications.update(is_read=True)
    return redirect('vue_d_ensemble')


@login_required
def delete_item(request, item_type, item_id):
    model = Task if item_type == 'task' else BugReport if item_type == 'bug' else None
    if not model:
        return HttpResponse("Type d'élément invalide", status=400)

    item = get_object_or_404(model, id=item_id)
    item.delete()
    return redirect('taches' if item_type == 'task' else 'bugs')


@login_required
def manage_item(request, item_type, item_id=None):
    if item_type == 'task':
        model = Task
        form_class = TaskForm
        redirect_url = 'taches'
    elif item_type == 'bug':
        model = BugReport
        form_class = BugReportForm
        redirect_url = 'bugs'
    else:
        return HttpResponse("Type d'élément invalide", status=400)

    item = get_object_or_404(model, id=item_id) if item_id else None
    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)  # Ne pas encore sauvegarder pour pouvoir ajouter les tags après
            item.save()  # Sauvegarde de l'instance pour lui donner un ID

            # Gestion des tags
            selected_tag_ids = request.POST.get('selected_tags', '').split(',')
            item.tags.set([int(tag_id) for tag_id in selected_tag_ids if tag_id])  # Mise à jour des tags

            return redirect(redirect_url)
    else:
        form = form_class(instance=item)

    context = {
        'form': form,
        'item_type': item_type,
        'title': "Modifier le bug" if item_id else "Créer un bug" if item_type == 'bug' else "Créer une tâche",
    }
    return render(request, 'gestion_projet/manage_item.html', context)

@login_required
def resolve_bug(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)

    if request.method == 'POST':
        form = BugResolutionForm(request.POST)
        if form.is_valid():
            bug.resolution_description = form.cleaned_data['resolution_description']
            bug.resolved_by = request.user
            bug.is_resolved = True
            bug.is_archived = True
            bug.save()
            return redirect('bugs')  # Redirige vers la liste des bugs une fois le bug résolu
    else:
        form = BugResolutionForm()

    return render(request, 'gestion_projet/resolve_bug.html', {'bug': bug, 'form': form})