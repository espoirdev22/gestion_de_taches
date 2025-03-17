from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Étudiant'),
        ('professor', 'Professeur'),
    )
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    
    def __str__(self):
        return self.username