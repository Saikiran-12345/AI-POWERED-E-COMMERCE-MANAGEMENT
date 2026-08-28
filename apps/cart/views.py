"""Cart views."""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem
from apps.products.models import Product, ProductStatus
from apps.audit.utils import log_action

logger = logging.getLogger('apps.cart')


def get_or_create_cart(request) -> Cart:
    """Get or create a cart for the current user or session."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    # Anonymous cart (session-based)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


@login_required
def cart_view(request):
    """Display the shopping cart."""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product', 'product__category', 'product__inventory')
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
    })


@login_required
@require_POST
def add_to_cart(request, product_id: int):
    """Add a product to the cart or update quantity if already present."""
    product = get_object_or_404(Product, pk=product_id, status=ProductStatus.ACTIVE)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        messages.error(request, 'Quantity must be at least 1.')
        return redirect('products:detail', slug=product.slug)

    # Check stock
    if product.stock_quantity < quantity:
        messages.error(
            request,
            f'Only {product.stock_quantity} units available.'
        )
        return redirect('products:detail', slug=product.slug)

    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'quantity': quantity,
            'price_at_add': product.discounted_price,
        }
    )

    if not created:
        new_qty = item.quantity + quantity
        if product.stock_quantity < new_qty:
            messages.error(
                request,
                f'Cannot add more. Only {product.stock_quantity} units available.'
            )
            return redirect('products:detail', slug=product.slug)
        item.quantity = new_qty
        item.save(update_fields=['quantity', 'updated_at'])
        messages.success(request, f'Updated quantity for "{product.name}" in your cart.')
    else:
        messages.success(request, f'"{product.name}" added to cart.')

    log_action(
        user=request.user,
        action='CART_ADD',
        module='cart',
        description=f'Added {quantity}x {product.name} to cart'
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_count': cart.total_items,
            'message': f'"{product.name}" added to cart.'
        })
    return redirect('cart:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id: int):
    """Remove an item from the cart."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    product_name = item.product.name
    item.delete()

    log_action(
        user=request.user,
        action='CART_REMOVE',
        module='cart',
        description=f'Removed {product_name} from cart'
    )

    messages.success(request, f'"{product_name}" removed from cart.')
    return redirect('cart:cart')


@login_required
@require_POST
def update_cart_quantity(request, item_id: int):
    """Update the quantity of a cart item."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        item.delete()
        messages.info(request, f'"{item.product.name}" removed from cart.')
    elif quantity > item.product.stock_quantity:
        messages.error(
            request,
            f'Only {item.product.stock_quantity} units of "{item.product.name}" available.'
        )
    else:
        item.quantity = quantity
        item.save(update_fields=['quantity', 'updated_at'])
        messages.success(request, 'Cart updated.')

    return redirect('cart:cart')


@login_required
@require_POST
def clear_cart(request):
    """Remove all items from the cart."""
    cart = get_or_create_cart(request)
    cart.clear()
    messages.info(request, 'Your cart has been cleared.')
    return redirect('cart:cart')
