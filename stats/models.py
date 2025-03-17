from django.db import models
from django.conf import settings
from decimal import Decimal


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
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # En pourcentage
    on_time_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # En pourcentage
    bonus_amount = models.IntegerField(default=0)  # En FCFA
    
    class Meta:
        unique_together = ('user', 'period', 'period_start', 'period_end')

    def calculer_prime(self):
        """ Calcule automatiquement la prime en fonction du taux d'achèvement. """
        if self.total_tasks_count == 0:
            self.completion_rate = Decimal('0.00')
            self.on_time_rate = Decimal('0.00')
            self.bonus_amount = 0
        else:
            # Calcul du taux d'achèvement et de ponctualité
            self.completion_rate = Decimal(self.completed_tasks_count) / Decimal(self.total_tasks_count) * 100
            self.on_time_rate = Decimal(self.on_time_tasks_count) / Decimal(self.total_tasks_count) * 100
            
            # Attribution de la prime en fonction du taux d'achèvement
            if self.completion_rate >= 100:
                self.bonus_amount = 100000  # 100% des tâches terminées
            elif self.completion_rate >= 90:
                self.bonus_amount = 30000  # Au moins 90% des tâches
            elif self.completion_rate >= 80:
                self.bonus_amount = 15000  # Entre 80% et 90%
            else:
                self.bonus_amount = 0  # Pas de prime

    def save(self, *args, **kwargs):
        """ Met à jour la prime et les taux uniquement si les valeurs ont changé. """
        # Récupérer l'ancien état avant la mise à jour
        if self.pk:
            old_instance = Performance.objects.get(pk=self.pk)
            if (
                self.completed_tasks_count != old_instance.completed_tasks_count or 
                self.total_tasks_count != old_instance.total_tasks_count or
                self.on_time_tasks_count != old_instance.on_time_tasks_count
            ):
                self.calculer_prime()  # Mettre à jour uniquement si les valeurs ont changé
        else:
            self.calculer_prime()  # Calcul initial

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.period} ({self.period_start} - {self.period_end})"
