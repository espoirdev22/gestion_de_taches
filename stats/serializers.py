from rest_framework import serializers
from .models import Performance
from users.serializers import UserSerializer

class PerformanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bonus = serializers.SerializerMethodField()  # Added computed field

    class Meta:
        model = Performance
        fields = [
            'id', 'user', 'period', 'period_start', 'period_end',
            'completed_tasks_count', 'on_time_tasks_count', 'total_tasks_count',
            'completion_rate', 'on_time_rate', 'bonus'
        ]
        read_only_fields = fields

    def get_bonus(self, obj):
        """ Calculates the bonus based on the task completion rate. """
        if obj.total_tasks_count == 0:  # Avoids division by zero
            return 0
        
        completion_rate = (obj.completed_tasks_count / obj.total_tasks_count) * 100
        
        if completion_rate == 100:
            return 100000  # Bonus of 100,000 FCFA
        elif completion_rate >= 90:
            return 30000  # Bonus of 30,000 FCFA
        return 0  # No bonus
