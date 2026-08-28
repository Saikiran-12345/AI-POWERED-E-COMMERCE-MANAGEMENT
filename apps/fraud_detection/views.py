from django.shortcuts import render
from apps.accounts.permissions import AdminRequiredMixin
from django.views.generic import TemplateView
from .models import FraudAnalysis

class FraudDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'fraud_detection/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['high_risk'] = FraudAnalysis.objects.filter(risk_level='HIGH', reviewed=False).select_related('order', 'user')
        ctx['medium_risk'] = FraudAnalysis.objects.filter(risk_level='MEDIUM', reviewed=False).select_related('order', 'user')[:20]
        return ctx
