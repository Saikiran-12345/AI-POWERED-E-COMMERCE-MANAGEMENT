from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from apps.accounts.permissions import CustomerRequiredMixin
from .models import Order, OrderStatus
from apps.audit.utils import log_action

@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Order.objects.filter(customer__user=user).order_by('-created_at')
        elif user.is_seller:
            from apps.orders.models import OrderItem
            order_ids = OrderItem.objects.filter(seller=user).values_list('order_id', flat=True)
            return Order.objects.filter(id__in=order_ids).order_by('-created_at')
        return Order.objects.all().order_by('-created_at')

@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'
    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Order.objects.filter(customer__user=user)
        return Order.objects.all()

@login_required
@require_POST
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    user = request.user
    if user.is_customer and order.customer.user != user:
        messages.error(request, 'Unauthorized.')
        return redirect('orders:list')
    try:
        order.cancel(reason='Cancelled by customer')
        log_action(user=user, action='ORDER_CANCEL', module='orders',
                   description=f'Order {order.order_number} cancelled', object_type='Order', object_id=pk)
        messages.success(request, f'Order #{order.order_number} cancelled.')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('orders:detail', pk=pk)
