# core/permissions.py
from rest_framework import permissions

class IsProjectCreator(permissions.BasePermission):
    """
    Permission qui n'autorise que le créateur du projet à le modifier/supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Lectures autorisées à tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Autorise seulement le créateur à modifier/supprimer
        return obj.created_by == request.user

class IsProjectMember(permissions.BasePermission):
    """
    Permission qui n'autorise que les membres du projet à y accéder.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est membre ou créateur du projet
        return (request.user in obj.members.all() or obj.created_by == request.user)

class IsTaskAssignee(permissions.BasePermission):
    """
    Permission qui n'autorise que l'assigné de la tâche à la mettre à jour.
    """
    def has_object_permission(self, request, view, obj):
        # Lectures autorisées à tous les membres du projet
        if request.method in permissions.SAFE_METHODS:
            return (request.user in obj.project.members.all() or 
                    obj.project.created_by == request.user)
        
        # Mise à jour autorisée pour l'assigné, le créateur de la tâche ou le créateur du projet
        return (obj.assigned_to == request.user or 
                obj.created_by == request.user or 
                obj.project.created_by == request.user)

class IsProfessor(permissions.BasePermission):
    """
    Permission qui n'autorise que les professeurs.
    """
    def has_permission(self, request, view):
        return request.user.user_type == 'professor'