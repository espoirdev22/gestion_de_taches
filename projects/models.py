from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('completed', 'Terminé'),
        ('archived', 'Archivé'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Accepte une description vide
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='member_projects',
        blank=True  # Permet d'avoir un projet sans membres au départ
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Trie les projets par date de création (du plus récent au plus ancien)
