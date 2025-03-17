from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'assigned_to', 'deadline', 'completed_at')
    list_filter = ('status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

