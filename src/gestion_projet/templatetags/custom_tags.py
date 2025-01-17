# custom_tags.py

from django import template
import re
from django.urls import reverse
from gestion_projet.models import Task, BugReport

register = template.Library()

@register.filter
def get_tag_by_id(tag_id):
    return Tag.objects.filter(id=tag_id).first()

@register.filter
def mention_links(message):
    # Chercher @task:<nom> et @bug:<nom>
    task_pattern = r'@task:([\w\s]+)'
    bug_pattern = r'@bug:([\w\s]+)'

    # Remplacer les mentions de tâche par des liens
    def task_link(match):
        task_name = match.group(1).strip()
        try:
            task = Task.objects.get(title=task_name)
            url = reverse('tache_detail', args=[task.id])
            return f'<a href="{url}">@task:{task_name}</a>'
        except Task.DoesNotExist:
            return f'@task:{task_name}'

    # Remplacer les mentions de bug par des liens
    def bug_link(match):
        bug_name = match.group(1).strip()
        try:
            bug = BugReport.objects.get(title=bug_name)
            url = reverse('bug_detail', args=[bug.id])
            return f'<a href="{url}">@bug:{bug_name}</a>'
        except BugReport.DoesNotExist:
            return f'@bug:{bug_name}'

    # Appliquer les transformations
    message = re.sub(task_pattern, task_link, message)
    message = re.sub(bug_pattern, bug_link, message)
    return message