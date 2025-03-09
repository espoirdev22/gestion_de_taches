from django.urls import path
from . import views  # Importer les vues de l'application


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
]
