from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, ProjectCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = []  # Aucune permission requise

    def get_queryset(self):
        return Project.objects.all()  # Permet d'afficher tous les projets sans restriction

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
            project.members.add(user)
            return Response({'status': 'member added'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
            if user == project.created_by:
                return Response(
                    {'error': 'Impossible de retirer le créateur du projet'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            project.members.remove(user)
            return Response({'status': 'member removed'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
