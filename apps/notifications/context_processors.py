"""Notification context processor."""

def notifications_context(request):
    """Inject unread notification count into every template."""
    unread_count = 0
    if request.user.is_authenticated:
        try:
            from .models import Notification
            unread_count = Notification.get_unread_count(request.user)
        except Exception:
            pass
    return {'unread_notification_count': unread_count}
