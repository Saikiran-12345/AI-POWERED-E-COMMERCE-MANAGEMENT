from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_admin:
        return redirect('dashboard:admin')
    elif user.is_seller:
        return redirect('dashboard:seller')
    return redirect('dashboard:customer')

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('dashboard:customer')
    from apps.analytics.views import get_analytics_data
    from apps.orders.models import Order, OrderStatus
    from apps.products.models import Product, ProductStatus
    from apps.customers.models import Customer
    from apps.sellers.models import SellerProfile
    from apps.inventory.models import Inventory
    from django.conf import settings
    low_stock = Inventory.objects.filter(quantity__lte=settings.LOW_STOCK_THRESHOLD).select_related('product')[:10]
    recent_orders = Order.objects.select_related('customer__user').order_by('-created_at')[:10]
    ctx = get_analytics_data()
    ctx.update({
        'low_stock_items': low_stock,
        'recent_orders': recent_orders,
        'total_sellers': SellerProfile.objects.count(),
        'total_active_products': Product.objects.filter(status=ProductStatus.ACTIVE).count(),
    })
    return render(request, 'dashboard/admin.html', ctx)

@login_required
def seller_dashboard(request):
    if not (request.user.is_seller or request.user.is_admin):
        return redirect('dashboard:customer')
    from apps.orders.models import Order, OrderItem, OrderStatus
    from apps.products.models import Product
    from apps.inventory.models import Inventory
    from django.db.models import Sum, Count
    from django.conf import settings
    seller = request.user
    my_products = Product.objects.filter(seller=seller)
    my_order_items = OrderItem.objects.filter(seller=seller)
    delivered_items = my_order_items.filter(order__status=OrderStatus.DELIVERED)
    low_stock = Inventory.objects.filter(
        product__seller=seller, quantity__lte=settings.LOW_STOCK_THRESHOLD
    ).select_related('product')[:10]
    ctx = {
        'my_products': my_products.count(),
        'total_orders': my_order_items.values('order').distinct().count(),
        'total_revenue': delivered_items.aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'low_stock_items': low_stock,
        'recent_products': my_products.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/seller.html', ctx)

@login_required
def customer_dashboard(request):
    from apps.orders.models import Order
    from apps.recommendations.models import Recommendation
    from apps.products.models import Product, ProductStatus
    customer = getattr(request.user, 'customer_profile', None)
    recent_orders = Order.objects.filter(customer=customer).order_by('-created_at')[:5] if customer else []
    recs = Recommendation.objects.filter(user=request.user).select_related('product')[:6]
    if not recs:
        rec_products = Product.objects.filter(status=ProductStatus.ACTIVE).order_by('-average_rating')[:6]
    else:
        rec_products = [r.product for r in recs]
    ctx = {
        'customer': customer,
        'recent_orders': recent_orders,
        'recommended_products': rec_products,
    }
    return render(request, 'dashboard/customer.html', ctx)
