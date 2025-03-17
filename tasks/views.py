from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from django.utils import timezone

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = []  # Suppression des permissions
    
    def get_queryset(self):
        user = self.request.user
        project_id = self.request.query_params.get('project')
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()  # Tout le monde peut voir toutes les tâches
    
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

        if old_status != new_status:
            if new_status == 'completed' and old_status != 'completed':
                updated_task.completed_at = timezone.now()
            elif old_status == 'completed' and new_status != 'completed':
                updated_task.completed_at = None
            updated_task.save()
    
    @action(detail=True, methods=['put'])
    def status(self, request, pk=None):
        task = self.get_object()
        old_status = task.status
        status_value = request.data.get('status')
        
        if status_value not in [choice[0] for choice in Task.STATUS_CHOICES]:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = status_value

        if status_value == 'completed' and old_status != 'completed':
            task.completed_at = timezone.now()
        elif old_status == 'completed' and status_value != 'completed':
            task.completed_at = None
        
        task.save()
        return Response(TaskSerializer(task).data)
