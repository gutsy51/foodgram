from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Subscription



@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'subscriber', 'created_at')
    list_filter = ('author', 'subscriber', 'created_at',)
    search_fields = ('author__username', 'subscriber__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


class FollowerInline(admin.TabularInline):
    """View subscribers of author."""
    model = Subscription
    fk_name = 'author'
    extra = 0
    verbose_name = _('Подписчик')
    verbose_name_plural = _('Подписчики')
    readonly_fields = ('created_at',)
    fields = ('subscriber', 'created_at')
    ordering = ('-created_at',)
    raw_id_fields = ('subscriber',)


class SubscriptionInline(admin.TabularInline):
    """View subscriptions of user."""
    model = Subscription
    fk_name = 'subscriber'
    extra = 0
    verbose_name = _('Подписка')
    verbose_name_plural = _('Подписки')
    readonly_fields = ('created_at',)
    fields = ('author', 'created_at')
    ordering = ('-created_at',)
    raw_id_fields = ('author',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [FollowerInline, SubscriptionInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    # Update the default form.
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')}
        ),
        (_('Персональные данные'), {
            'fields': ('first_name', 'last_name', 'avatar',
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
