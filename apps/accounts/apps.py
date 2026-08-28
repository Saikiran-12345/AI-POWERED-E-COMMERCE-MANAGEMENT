"""
Accounts app configuration.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Accounts'

    def ready(self):
        """Import signal handlers when app is ready."""
        import apps.accounts.signals  # noqa: F401
