"""Wishlist views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Wishlist, WishlistItem
from apps.products.models import Product, ProductStatus
from apps.audit.utils import log_action


def get_customer(request):
    """Get the customer profile for the current user."""
    try:
        return request.user.customer_profile
    except Exception:
        return None


@login_required
def wishlist_view(request):
    """Display user's wishlist."""
    customer = get_customer(request)
    if not customer:
        messages.error(request, 'Customer profile not found.')
        return redirect('products:list')

    wishlist, _ = Wishlist.objects.get_or_create(customer=customer)
    items = wishlist.items.select_related(
        'product', 'product__category', 'product__inventory'
    ).order_by('-added_at')

    return render(request, 'wishlist/wishlist.html', {
        'wishlist': wishlist,
        'items': items,
    })


@login_required
@require_POST
def add_to_wishlist(request, product_id: int):
    """Add a product to wishlist."""
    customer = get_customer(request)
    if not customer:
        messages.error(request, 'Please complete your profile first.')
        return redirect('products:list')

    product = get_object_or_404(Product, pk=product_id, status=ProductStatus.ACTIVE)
    wishlist, _ = Wishlist.objects.get_or_create(customer=customer)

    _, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

    if created:
        log_action(
            user=request.user,
            action='WISHLIST_ADD',
            module='wishlist',
            description=f'Added {product.name} to wishlist'
        )
        messages.success(request, f'"{product.name}" added to wishlist.')
    else:
        messages.info(request, f'"{product.name}" is already in your wishlist.')

    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))


@login_required
@require_POST
def remove_from_wishlist(request, item_id: int):
    """Remove a product from wishlist."""
    customer = get_customer(request)
    if not customer:
        return redirect('wishlist:wishlist')

    item = get_object_or_404(WishlistItem, pk=item_id, wishlist__customer=customer)
    product_name = item.product.name
    item.delete()

    log_action(
        user=request.user,
        action='WISHLIST_REMOVE',
        module='wishlist',
        description=f'Removed {product_name} from wishlist'
    )
    messages.success(request, f'"{product_name}" removed from wishlist.')
    return redirect('wishlist:wishlist')


@login_required
@require_POST
def move_to_cart(request, item_id: int):
    """Move a wishlist item to the shopping cart."""
    customer = get_customer(request)
    if not customer:
        return redirect('wishlist:wishlist')

    item = get_object_or_404(WishlistItem, pk=item_id, wishlist__customer=customer)
    product = item.product

    if not product.is_in_stock:
        messages.error(request, f'"{product.name}" is currently out of stock.')
        return redirect('wishlist:wishlist')

    from apps.cart.views import get_or_create_cart
    from apps.cart.models import CartItem
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'quantity': 1,
            'price_at_add': product.discounted_price,
        }
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])

    item.delete()
    messages.success(request, f'"{product.name}" moved to cart.')
    return redirect('cart:cart')
