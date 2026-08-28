from django.shortcuts import render
from apps.accounts.permissions import AdminRequiredMixin
from django.views.generic import TemplateView
from .models import DemandForecast

class ForecastDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'forecasting/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['forecasts'] = DemandForecast.objects.order_by('-created_at', 'forecast_date')[:50]
        return ctx
