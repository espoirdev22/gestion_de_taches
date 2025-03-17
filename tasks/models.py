from django.db import models
from django.conf import settings
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = (
        ('to_do', 'À faire'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='to_do')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

