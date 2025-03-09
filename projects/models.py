from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects",
        blank=True, null=True  
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="project_members")

    def __str__(self):
        return self.title
