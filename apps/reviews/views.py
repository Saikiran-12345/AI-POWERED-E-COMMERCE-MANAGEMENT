from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Review
from apps.products.models import Product

@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    customer = getattr(request.user, 'customer_profile', None)
    if not customer:
        messages.error(request, 'Customer profile required.')
        return redirect('products:detail', slug=product.slug)
    rating = int(request.POST.get('rating', 5))
    title = request.POST.get('title', '')
    body = request.POST.get('body', '')
    if not body:
        messages.error(request, 'Review text is required.')
        return redirect('products:detail', slug=product.slug)
    Review.objects.update_or_create(
        product=product, customer=customer,
        defaults={'rating': rating, 'title': title, 'body': body}
    )
    messages.success(request, 'Review submitted.')
    return redirect('products:detail', slug=product.slug)
