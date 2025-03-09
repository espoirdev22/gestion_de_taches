from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskHistorySerializer
from core.permissions import IsTaskAssignee
from django.utils import timezone

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskAssignee]
    
    def get_queryset(self):
        user = self.request.user
        # Filtrer par projet si fourni
        project_id = self.request.query_params.get('project')
        if project_id:
            return Task.objects.filter(project_id=project_id)
        
        # Sinon retourner toutes les tâches accessibles à l'utilisateur
        return Task.objects.filter(
            project__members=user
        ) | Task.objects.filter(
            project__created_by=user
        ) | Task.objects.filter(
            assigned_to=user
        ).distinct()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        task = self.get_object()
        old_status = task.status
        updated_task = serializer.save()
        new_status = updated_task.status
        
        # Si le statut a changé, créer une entrée dans l'historique
        if old_status != new_status:
            # Si la tâche est marquée comme terminée, enregistrer la date d'achèvement
            if new_status == 'completed' and old_status != 'completed':
                updated_task.completed_at = timezone.now()
                updated_task.save()
            # Si la tâche est passée de terminée à un autre statut, effacer la date d'achèvement
            elif old_status == 'completed' and new_status != 'completed':
                updated_task.completed_at = None
                updated_task.save()
            
            TaskHistory.objects.create(
                task=updated_task,
                previous_status=old_status,
                new_status=new_status,
                changed_by=self.request.user
            )
    
    @action(detail=True, methods=['put'])
    def status(self, request, pk=None):
        task = self.get_object()
        old_status = task.status
        status_value = request.data.get('status')
        
        if status_value not in [choice[0] for choice in Task.STATUS_CHOICES]:
            return Response(
                {'error': 'Statut invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = status_value
        
        # Si la tâche est marquée comme terminée, enregistrer la date d'achèvement
        if status_value == 'completed' and old_status != 'completed':
            task.completed_at = timezone.now()
        # Si la tâche est passée de terminée à un autre statut, effacer la date d'achèvement
        elif old_status == 'completed' and status_value != 'completed':
            task.completed_at = None
        
        task.save()
        
        # Créer une entrée dans l'historique
        TaskHistory.objects.create(
            task=task,
            previous_status=old_status,
            new_status=status_value,
            changed_by=request.user
        )
        
        return Response(TaskSerializer(task).data)

class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.request.query_params.get('task')
        if task_id:
            return TaskHistory.objects.filter(task_id=task_id).order_by('-changed_at')
        return TaskHistory.objects.none()