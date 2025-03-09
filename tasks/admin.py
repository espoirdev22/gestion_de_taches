from django.contrib import admin
from .models import Task, TaskHistory

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'assigned_to', 'deadline', 'completed_at')
    list_filter = ('status', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('task', 'previous_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('previous_status', 'new_status', 'changed_at')
    date_hierarchy = 'changed_at'