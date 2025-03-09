from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('avatar', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)