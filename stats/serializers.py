from rest_framework import serializers
from .models import Performance
from users.serializers import UserSerializer

class PerformanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = [
            'id', 'user', 'period', 'period_start', 'period_end',
            'completed_tasks_count', 'on_time_tasks_count', 'total_tasks_count',
            'completion_rate', 'on_time_rate', 'bonus_amount'
        ]
        read_only_fields = fields
