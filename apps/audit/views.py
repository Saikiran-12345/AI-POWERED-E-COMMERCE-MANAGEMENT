"""
Views for the audit application.
"""

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.permissions import AdminRequiredMixin
from .models import AuditLog


class AuditLogListView(AdminRequiredMixin, ListView):
    """Admin-only view listing all audit logs."""

    model = AuditLog
    template_name = 'audit/list.html'
    context_object_name = 'logs'
    paginate_by = 50

    def get_queryset(self):
        qs = AuditLog.objects.select_related('user').order_by('-timestamp')
        action = self.request.GET.get('action')
        module = self.request.GET.get('module')
        user_id = self.request.GET.get('user')

        if action:
            qs = qs.filter(action=action)
        if module:
            qs = qs.filter(module=module)
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_choices'] = AuditLog.ACTION_CHOICES
        ctx['selected_action'] = self.request.GET.get('action', '')
        ctx['selected_module'] = self.request.GET.get('module', '')
        return ctx


class AuditLogDetailView(AdminRequiredMixin, DetailView):
    """Admin-only view for a single audit log entry."""

    model = AuditLog
    template_name = 'audit/detail.html'
    context_object_name = 'log'
