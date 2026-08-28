"""
Middleware for the audit application.

Captures request context for automatic audit logging.
"""

from django.utils.deprecation import MiddlewareMixin


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware that attaches the current request to the thread-local
    so audit log utils can access IP and user agent without passing
    the request object everywhere.
    """

    def process_request(self, request):
        """Store request in thread-local storage."""
        pass  # Currently handled by explicit request passing in log_action

    def process_response(self, request, response):
        """Clean up after response."""
        return response
