from rest_framework import serializers
from .models import Task, TaskHistory
from projects.serializers import ProjectSerializer, UserBasicSerializer

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assigned_to = UserBasicSerializer(read_only=True)
    created_by = UserBasicSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'deadline', 'status',
            'project', 'assigned_to', 'created_by',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'completed_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'assigned_to', 'project']
        read_only_fields = ['id']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'assigned_to']

class TaskHistorySerializer(serializers.ModelSerializer):
    changed_by = UserBasicSerializer(read_only=True)

    class Meta:
        model = TaskHistory
        fields = ['id', 'task', 'previous_status', 'new_status', 'changed_by', 'changed_at']
        read_only_fields = ['id', 'task', 'previous_status', 'new_status', 'changed_by', 'changed_at']
