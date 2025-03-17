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
        fields = ['id', 'title', 'description', 'status', 'created_by', 'created_at', 'updated_at', 'members']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False, validators=[]
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'members']
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Utilisateur non authentifié.")

        members = validated_data.pop('members', [])
        project = Project.objects.create(created_by=user, **validated_data)
        project.members.set(members)  
        return project
