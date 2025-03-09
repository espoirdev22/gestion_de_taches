from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Performance
from .serializers import PerformanceSerializer
from core.permissions import IsProfessor
from datetime import datetime, timedelta
from django.db.models import Q

class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerformanceSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAuthenticated, IsProfessor]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        period = self.request.query_params.get('period', 'trimester')
        
        # Si professeur, accès à toutes les performances
        if user.user_type == 'professor':
            return Performance.objects.filter(period=period)
        
        # Sinon, uniquement ses propres performances
        return Performance.objects.filter(user=user, period=period)
    
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        period = request.query_params.get('period', 'trimester')
        performances = Performance.objects.filter(user=request.user, period=period)
        serializer = self.get_serializer(performances, many=True)
        return Response(serializer.data)
