from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Performance
from .serializers import PerformanceSerializer

class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = []  # Suppression des permissions
    
    def get_queryset(self):
        period = self.request.query_params.get('period', 'trimester')
        return Performance.objects.filter(period=period)  # Tout le monde peut voir toutes les performances
    
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        period = request.query_params.get('period', 'trimester')
        performances = Performance.objects.filter(period=period)
        serializer = self.get_serializer(performances, many=True)
        return Response(serializer.data)
