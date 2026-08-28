from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.accounts.permissions import admin_required
from django.utils import timezone
from datetime import timedelta

@login_required
def analytics_overview(request):
    return render(request, 'analytics/overview.html', get_analytics_data())

def get_analytics_data():
    from apps.orders.models import Order, OrderStatus
    from apps.products.models import Product
    from apps.accounts.models import User
    from apps.customers.models import Customer
    from django.db.models import Sum, Count, Avg
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    completed_orders = Order.objects.filter(status__in=[OrderStatus.DELIVERED, OrderStatus.SHIPPED])
    recent_orders = completed_orders.filter(created_at__gte=thirty_days_ago)
    return {
        'total_orders': Order.objects.count(),
        'total_revenue': completed_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_products': Product.objects.count(),
        'total_customers': Customer.objects.count(),
        'recent_revenue': recent_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'recent_orders': recent_orders.count(),
    }
