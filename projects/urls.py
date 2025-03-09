from django.urls import path
from .views import project_list, project_create, project_update, project_delete

urlpatterns = [
    path('', project_list, name='project_list'),
    path('create/', project_create, name='project_create'),
    path('update/<int:pk>/', project_update, name='project_update'),
    path('delete/<int:pk>/', project_delete, name='project_delete'),
]