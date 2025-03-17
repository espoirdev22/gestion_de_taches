from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from tasks.models import Task
from .models import Performance
from django.db.models import Q, Count, Case, When, IntegerField
from django.contrib.auth import get_user_model

User = get_user_model()

def get_period_dates(period_type='trimester', target_date=None):
    """
    Retourne les dates de début et de fin pour une période donnée
    """
    if target_date is None:
        target_date = date.today()
    
    if period_type == 'trimester':
        # Déterminer le trimestre actuel
        month = target_date.month
        if month <= 3:
            start_date = date(target_date.year, 1, 1)
            end_date = date(target_date.year, 3, 31)
        elif month <= 6:
            start_date = date(target_date.year, 4, 1)
            end_date = date(target_date.year, 6, 30)
        elif month <= 9:
            start_date = date(target_date.year, 7, 1)
            end_date = date(target_date.year, 9, 30)
        else:
            start_date = date(target_date.year, 10, 1)
            end_date = date(target_date.year, 12, 31)
    else:  # yearly
        start_date = date(target_date.year, 1, 1)
        end_date = date(target_date.year, 12, 31)
    
    return start_date, end_date

def calculate_performances(period_type='trimester', target_date=None):
    """
    Calcule les performances pour tous les utilisateurs pour une période donnée
    """
    if target_date is None:
        target_date = date.today()
    
    start_date, end_date = get_period_dates(period_type, target_date)
    
    # Récupérer tous les utilisateurs
    users = User.objects.filter(user_type='student')
    
    for user in users:
        # Récupérer les tâches assignées à l'utilisateur pendant la période
        tasks = Task.objects.filter(
            assigned_to=user,
            deadline__gte=start_date,
            deadline__lte=end_date
        )
        
        total_count = tasks.count()
        
        if total_count == 0:
            continue  # Passer à l'utilisateur suivant s'il n'a pas de tâches
        
        # Compter les tâches terminées
        completed_count = tasks.filter(status='completed').count()
        
        # Compter les tâches terminées à temps
        on_time_count = tasks.filter(
            status='completed',
            completed_at__isnull=False,
            completed_at__lte=Q(deadline=F('deadline'))
        ).count()
        
        # Calculer les taux
        completion_rate = (completed_count / total_count) * 100 if total_count > 0 else 0
        on_time_rate = (on_time_count / completed_count) * 100 if completed_count > 0 else 0
        
        # Calculer la prime
        bonus_amount = 0
        if on_time_rate >= 90:
            bonus_amount = 30000
        if on_time_rate == 100:
            bonus_amount = 100000
        
        # Sauvegarder ou mettre à jour la performance
        performance, created = Performance.objects.update_or_create(
            user=user,
            period=period_type,
            period_start=start_date,
            period_end=end_date,
            defaults={
                'completed_tasks_count': completed_count,
                'on_time_tasks_count': on_time_count,
                'total_tasks_count': total_count,
                'completion_rate': completion_rate,
                'on_time_rate': on_time_rate,
                'bonus_amount': bonus_amount
            }
        )
    
    return True