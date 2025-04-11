from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Table display settings.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)

    # Update the default form.
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')}
        ),
        (_('Персональные данные'), {
            'fields': ('first_name', 'last_name', 'profile_picture',
                       'last_login', 'date_joined'),
        }),
        (_('Права'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
    )

    # Add first and last name fields in the Add form.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name',
                       'password1', 'password2'),
        }),
    )
