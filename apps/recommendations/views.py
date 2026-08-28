from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Recommendation
from apps.products.models import Product, ProductStatus

@login_required
def recommendations_view(request):
    recs = Recommendation.objects.filter(user=request.user).select_related('product', 'product__category')[:20]
    if not recs:
        # Fallback: show popular products
        products = Product.objects.filter(status=ProductStatus.ACTIVE).order_by('-purchase_count', '-average_rating')[:20]
    else:
        products = [r.product for r in recs]
    return render(request, 'recommendations/list.html', {'recommended_products': products, 'recs': recs})
