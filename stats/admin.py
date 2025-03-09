from django.contrib import admin
from .models import Performance

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'period_start', 'period_end', 'completion_rate', 'on_time_rate', 'bonus_amount')
    list_filter = ('period', 'period_start', 'period_end')
    search_fields = ('user__username', 'user__email')