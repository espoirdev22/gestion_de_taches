from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    filter_horizontal = ('members',)
def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user  
        obj.save()