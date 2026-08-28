from django.shortcuts import render
from apps.accounts.permissions import AdminRequiredMixin, SellerOrAdminRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

@login_required
def reports_dashboard(request):
    return render(request, 'reports/dashboard.html', {'title': 'Reports'})

@login_required
def sales_report(request):
    from apps.orders.models import Order, OrderStatus
    from django.db.models import Sum, Count
    days = int(request.GET.get('days', 30))
    since = timezone.now() - timedelta(days=days)
    orders = Order.objects.filter(created_at__gte=since).filter(status__in=[OrderStatus.DELIVERED, OrderStatus.SHIPPED])
    stats = orders.aggregate(total_revenue=Sum('total_amount'), total_orders=Count('id'), avg_order=Sum('total_amount'))
    return render(request, 'reports/sales.html', {'orders': orders[:100], 'stats': stats, 'days': days})
