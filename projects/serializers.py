from rest_framework import serializers
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserBasicSerializer(read_only=True)
    members = UserBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at', 'members']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']
