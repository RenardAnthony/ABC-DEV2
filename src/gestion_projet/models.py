from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField  # Utilisé si vous basculez vers PostgreSQL
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    progress = models.IntegerField(default=0)
    priority = models.CharField(max_length=20, choices=[('Haute', 'Haute'), ('Moyenne', 'Moyenne'), ('Basse', 'Basse')])
    tags = models.ManyToManyField("Tag", blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks_assigned"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_created"
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class BugReport(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, choices=[('Haute', 'Haute'), ('Moyenne', 'Moyenne'), ('Basse', 'Basse')])
    tags = models.ManyToManyField(Tag, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="bugs_assigned"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="bugs_created"
    )
    created_at = models.DateTimeField(default=timezone.now)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_bugs"
    )
    resolution_description = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='task_messages')
    bug = models.ForeignKey(BugReport, on_delete=models.CASCADE, null=True, blank=True, related_name='bug_messages')

class ActivityLog(models.Model):
    action = models.CharField(max_length=100)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    bug = models.ForeignKey(BugReport, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    bug = models.ForeignKey(BugReport, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user} on {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}: {self.message}"
