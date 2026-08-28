"""
Utility functions for audit logging.
"""

import logging
from typing import Optional, Dict, Any
from django.conf import settings

logger = logging.getLogger('apps.audit')


def log_action(
    user=None,
    action: str = 'SYSTEM',
    module: str = 'system',
    description: str = '',
    object_type: str = '',
    object_id: str = '',
    extra_data: Optional[Dict[str, Any]] = None,
    request=None,
) -> None:
    """
    Create an audit log entry.

    Args:
        user: The User instance who performed the action (None for system actions).
        action: The action code (must match AuditLog.ACTION_CHOICES).
        module: The application module name.
        description: Human-readable description of the action.
        object_type: The type of object affected (e.g., 'Product').
        object_id: The ID of the affected object.
        extra_data: Additional JSON-serializable data.
        request: Django request object (to extract IP and user agent).
    """
    try:
        from .models import AuditLog

        ip_address = None
        user_agent = ''

        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

        AuditLog.objects.create(
            user=user,
            action=action,
            module=module,
            description=description,
            object_type=object_type,
            object_id=str(object_id) if object_id else '',
            extra_data=extra_data or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
    except Exception as e:
        # Never let audit logging break the application
        logger.error(f'Failed to create audit log: {e}')
