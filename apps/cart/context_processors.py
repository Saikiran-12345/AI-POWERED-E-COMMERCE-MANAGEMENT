"""Cart context processor — provides cart count to all templates."""

def cart_context(request):
    """Inject cart item count into every template context."""
    cart_count = 0
    if request.user.is_authenticated:
        try:
            from .models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_count = cart.total_items
        except Exception:
            pass
    return {'cart_count': cart_count}
