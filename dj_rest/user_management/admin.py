# user_management/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ('username', 'email', 'tg_username')
    list_filter = ('is_staff', 'is_active', 'tg_username')
    list_display = ('username', 'email', 'tg_username', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'tg_id', 'tg_username')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'tg_id', 'tg_username')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
