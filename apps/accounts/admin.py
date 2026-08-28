"""
Django admin configuration for the accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, LoginHistory


class UserProfileInline(admin.StackedInline):
    """Inline admin for user profiles."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = (
        'bio', 'date_of_birth', 'gender',
        'address_line1', 'address_line2', 'city', 'state', 'pincode', 'country',
        'newsletter_subscribed', 'email_notifications',
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin panel configuration for the custom User model."""

    inlines = (UserProfileInline,)
    list_display = (
        'email', 'first_name', 'last_name', 'role',
        'is_active', 'is_staff', 'date_joined'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'phone_number', 'avatar')
        }),
        (_('Role & Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        (_('Important Dates'), {
            'fields': ('date_joined', 'last_login', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'role',
                'password1', 'password2'
            ),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    list_display = ('user', 'city', 'country', 'newsletter_subscribed')
    search_fields = ('user__email', 'user__first_name', 'city')
    list_filter = ('country', 'newsletter_subscribed')


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin for login history."""
    list_display = ('user', 'login_time', 'logout_time', 'ip_address', 'was_successful')
    list_filter = ('was_successful', 'login_time')
    search_fields = ('user__email', 'ip_address')
    readonly_fields = ('user', 'login_time', 'ip_address', 'user_agent', 'session_key')
    ordering = ('-login_time',)
