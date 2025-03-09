from django.db import models
from django.conf import settings

class Performance(models.Model):
    PERIOD_CHOICES = (
        ('trimester', 'Trimestre'),
        ('year', 'Année'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performances')
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    completed_tasks_count = models.IntegerField(default=0)
    on_time_tasks_count = models.IntegerField(default=0)
    total_tasks_count = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0)  # En pourcentage
    on_time_rate = models.FloatField(default=0)  # En pourcentage
    bonus_amount = models.IntegerField(default=0)  # En FCFA
    
    class Meta:
        unique_together = ('user', 'period', 'period_start', 'period_end')
    
    def __str__(self):
        return f"{self.user.username} - {self.period} ({self.period_start} - {self.period_end})"