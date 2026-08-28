from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Payment, PaymentMethod, PaymentStatus
from apps.orders.models import Order, OrderStatus
from apps.notifications.models import Notification
from apps.audit.utils import log_action

@login_required
def checkout_view(request):
    from apps.cart.views import get_or_create_cart
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart')
    profile = getattr(request.user, 'profile', None)
    return render(request, 'payments/checkout.html', {
        'cart': cart,
        'items': cart.items.select_related('product'),
        'profile': profile,
        'payment_methods': PaymentMethod.choices,
    })

@login_required
@require_POST
def process_payment(request):
    from apps.cart.views import get_or_create_cart
    from apps.orders.models import OrderItem
    from django.db import transaction
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.error(request, 'Cart is empty.')
        return redirect('cart:cart')
    customer = getattr(request.user, 'customer_profile', None)
    if not customer:
        messages.error(request, 'Customer profile required.')
        return redirect('accounts:profile')
    method = request.POST.get('payment_method', PaymentMethod.CASH_ON_DELIVERY)
    try:
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                subtotal=cart.subtotal,
                total_amount=cart.total,
                shipping_name=request.user.get_full_name(),
                shipping_email=request.user.email,
                shipping_address1=request.POST.get('address1', ''),
                shipping_city=request.POST.get('city', ''),
                shipping_state=request.POST.get('state', ''),
                shipping_pincode=request.POST.get('pincode', ''),
            )
            for item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    unit_price=item.product.discounted_price,
                    total_price=item.total_price,
                    seller=item.product.seller,
                )
                item.product.inventory.reduce_stock(item.quantity)
            payment = Payment.objects.create(
                order=order,
                amount=order.total_amount,
                method=method,
            )
            success = payment.process_mock_payment()
            if success:
                order.status = OrderStatus.CONFIRMED
                order.save(update_fields=['status'])
                cart.clear()
                Notification.create_notification(
                    user=request.user,
                    notification_type='ORDER_CONFIRMED',
                    title=f'Order #{order.order_number} Confirmed!',
                    message=f'Your order has been confirmed. Total: {order.total_amount}',
                    link=f'/orders/{order.pk}/',
                )
                log_action(user=request.user, action='ORDER_CREATE', module='orders',
                           description=f'Order {order.order_number} created', object_type='Order', object_id=order.pk)
                messages.success(request, f'Order #{order.order_number} placed successfully!')
                return redirect('orders:detail', pk=order.pk)
            else:
                order.cancel('Payment failed')
                messages.error(request, 'Payment failed. Please try again.')
                return redirect('cart:cart')
    except Exception as e:
        messages.error(request, f'Order creation failed: {str(e)}')
        return redirect('cart:cart')
