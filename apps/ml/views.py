from django.shortcuts import render
from apps.accounts.permissions import AdminRequiredMixin
from django.views.generic import TemplateView

class MLDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'ml/dashboard.html'
    def get_context_data(self, **kwargs):
        from .models import MLModel
        ctx = super().get_context_data(**kwargs)
        ctx['models'] = MLModel.objects.filter(is_active=True)
        return ctx
