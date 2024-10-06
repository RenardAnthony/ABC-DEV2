from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    PRIORITY_LEVELS = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)  # Nouveau champ pour l'archivage
    priority = models.CharField(max_length=1, choices=PRIORITY_LEVELS, default='M')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
