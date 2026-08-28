"""
Views for the products application.

Includes product listing, detail, CRUD for sellers/admins,
category management, and search functionality.
"""

import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Product, Category, ProductStatus, ProductImage, ProductAttribute
from .forms import ProductForm, CategoryForm, ProductSearchForm
from apps.accounts.permissions import (
    SellerRequiredMixin, AdminRequiredMixin,
    SellerOrAdminRequiredMixin, seller_required, admin_required
)
from apps.audit.utils import log_action

logger = logging.getLogger('apps.products')


class ProductListView(ListView):
    """
    Public product listing with search, filtering, and pagination.
    """
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        qs = Product.objects.filter(
            status=ProductStatus.ACTIVE
        ).select_related('category', 'seller').prefetch_related('inventory')

        form = ProductSearchForm(self.request.GET)
        if not form.is_valid():
            return qs

        # Keyword search
        q = form.cleaned_data.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(brand__icontains=q) |
                Q(tags__icontains=q) |
                Q(category__name__icontains=q)
            )

        # Category filter
        category = form.cleaned_data.get('category')
        if category:
            qs = qs.filter(category=category)

        # Brand filter
        brand = form.cleaned_data.get('brand')
        if brand:
            qs = qs.filter(brand__icontains=brand)

        # Price filters
        min_price = form.cleaned_data.get('min_price')
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)

        max_price = form.cleaned_data.get('max_price')
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        # Rating filter
        min_rating = form.cleaned_data.get('min_rating')
        if min_rating:
            qs = qs.filter(average_rating__gte=float(min_rating))

        # In-stock filter
        in_stock = form.cleaned_data.get('in_stock')
        if in_stock:
            qs = qs.filter(inventory__quantity__gt=0)

        # Sorting
        sort_by = form.cleaned_data.get('sort_by')
        sort_map = {
            'price_asc': 'price',
            'price_desc': '-price',
            'rating': '-average_rating',
            'newest': '-created_at',
            'popular': '-purchase_count',
        }
        if sort_by and sort_by in sort_map:
            qs = qs.order_by(sort_map[sort_by])

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ProductSearchForm(self.request.GET)
        ctx['categories'] = Category.objects.filter(is_active=True, parent=None)
        ctx['featured_products'] = Product.objects.filter(
            status=ProductStatus.ACTIVE, is_featured=True
        ).select_related('category')[:8]
        ctx['total_count'] = self.get_queryset().count()
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class ProductDetailView(DetailView):
    """
    Public product detail page with reviews and recommendations.
    """
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        # Increment view count (non-blocking)
        product.increment_view_count()
        return product

    def get_queryset(self):
        return Product.objects.filter(
            status=ProductStatus.ACTIVE
        ).select_related('category', 'seller', 'inventory')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = self.object

        # Reviews
        ctx['reviews'] = product.reviews.filter(
            is_approved=True
        ).select_related('customer__user').order_by('-created_at')[:10]

        # Product images
        ctx['product_images'] = product.images.all()

        # Product attributes
        ctx['product_attributes'] = product.attributes.all()

        # Related products (same category)
        ctx['related_products'] = Product.objects.filter(
            category=product.category,
            status=ProductStatus.ACTIVE
        ).exclude(pk=product.pk).select_related('category')[:8]

        # Wishlist check
        if self.request.user.is_authenticated and self.request.user.is_customer:
            try:
                from apps.wishlist.models import Wishlist
                wishlist = Wishlist.objects.filter(customer__user=self.request.user).first()
                if wishlist:
                    ctx['in_wishlist'] = wishlist.items.filter(product=product).exists()
                else:
                    ctx['in_wishlist'] = False
            except Exception:
                ctx['in_wishlist'] = False

        # Can review?
        ctx['can_review'] = False
        if self.request.user.is_authenticated and self.request.user.is_customer:
            try:
                from apps.orders.models import OrderItem, OrderStatus
                ctx['can_review'] = OrderItem.objects.filter(
                    order__customer__user=self.request.user,
                    order__status__in=[OrderStatus.DELIVERED],
                    product=product
                ).exists()
            except Exception:
                pass

        return ctx


class CategoryDetailView(ListView):
    """Products filtered by category."""
    model = Product
    template_name = 'products/category.html'
    context_object_name = 'products'
    paginate_by = 16

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Product.objects.filter(
            category=self.category,
            status=ProductStatus.ACTIVE
        ).select_related('seller')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = self.category
        ctx['subcategories'] = self.category.children.filter(is_active=True)
        return ctx


# -------------------------------------------------------------------
# Seller Product Management Views
# -------------------------------------------------------------------

class SellerProductListView(SellerOrAdminRequiredMixin, ListView):
    """Seller's own product management page."""
    model = Product
    template_name = 'products/seller/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Product.objects.select_related('category', 'seller').order_by('-created_at')
        return Product.objects.filter(
            seller=user
        ).select_related('category').order_by('-created_at')


class ProductCreateView(SellerOrAdminRequiredMixin, CreateView):
    """Create a new product."""
    model = Product
    form_class = ProductForm
    template_name = 'products/seller/form.html'
    success_url = reverse_lazy('products:seller_list')

    def form_valid(self, form):
        product = form.save(commit=False)
        if self.request.user.is_seller:
            product.seller = self.request.user
        elif 'seller_id' in self.request.POST:
            from apps.accounts.models import User
            product.seller_id = self.request.POST.get('seller_id')
        product.save()

        # Create default inventory record
        from apps.inventory.models import Inventory
        stock = int(self.request.POST.get('initial_stock', 0))
        Inventory.objects.create(product=product, quantity=stock)

        log_action(
            user=self.request.user,
            action='PRODUCT_CREATE',
            module='products',
            description=f'Product created: {product.name}',
            object_type='Product',
            object_id=product.pk
        )

        messages.success(self.request, f'Product "{product.name}" created successfully.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Add New Product'
        ctx['submit_label'] = 'Create Product'
        return ctx


class ProductUpdateView(SellerOrAdminRequiredMixin, UpdateView):
    """Update an existing product."""
    model = Product
    form_class = ProductForm
    template_name = 'products/seller/form.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            return Product.objects.all()
        return Product.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        product = form.save()
        log_action(
            user=self.request.user,
            action='PRODUCT_UPDATE',
            module='products',
            description=f'Product updated: {product.name}',
            object_type='Product',
            object_id=product.pk
        )
        messages.success(self.request, f'Product "{product.name}" updated successfully.')
        return redirect('products:seller_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Edit: {self.object.name}'
        ctx['submit_label'] = 'Save Changes'
        return ctx


class ProductDeleteView(SellerOrAdminRequiredMixin, DeleteView):
    """Delete a product."""
    model = Product
    template_name = 'products/seller/confirm_delete.html'
    success_url = reverse_lazy('products:seller_list')

    def get_queryset(self):
        if self.request.user.is_admin:
            return Product.objects.all()
        return Product.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        product = self.get_object()
        log_action(
            user=self.request.user,
            action='PRODUCT_DELETE',
            module='products',
            description=f'Product deleted: {product.name}',
            object_type='Product',
            object_id=product.pk
        )
        messages.success(self.request, f'Product "{product.name}" deleted.')
        return super().form_valid(form)


# -------------------------------------------------------------------
# Category Management (Admin only)
# -------------------------------------------------------------------

class CategoryListView(AdminRequiredMixin, ListView):
    """Admin category management."""
    model = Category
    template_name = 'products/admin/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(
            num_products=Count('products')
        ).order_by('sort_order', 'name')


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Create a new category."""
    model = Category
    form_class = CategoryForm
    template_name = 'products/admin/category_form.html'
    success_url = reverse_lazy('products:category_list')

    def form_valid(self, form):
        category = form.save()
        log_action(
            user=self.request.user,
            action='CATEGORY_CREATE',
            module='products',
            description=f'Category created: {category.name}',
            object_type='Category',
            object_id=category.pk
        )
        messages.success(self.request, f'Category "{category.name}" created.')
        return redirect(self.success_url)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Update a category."""
    model = Category
    form_class = CategoryForm
    template_name = 'products/admin/category_form.html'
    success_url = reverse_lazy('products:category_list')

    def form_valid(self, form):
        category = form.save()
        log_action(
            user=self.request.user,
            action='CATEGORY_UPDATE',
            module='products',
            description=f'Category updated: {category.name}',
            object_type='Category',
            object_id=category.pk
        )
        messages.success(self.request, f'Category "{category.name}" updated.')
        return redirect(self.success_url)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a category."""
    model = Category
    template_name = 'products/admin/category_confirm_delete.html'
    success_url = reverse_lazy('products:category_list')

    def form_valid(self, form):
        category = self.get_object()
        log_action(
            user=self.request.user,
            action='CATEGORY_DELETE',
            module='products',
            description=f'Category deleted: {category.name}',
            object_type='Category',
            object_id=category.pk
        )
        messages.success(self.request, f'Category "{category.name}" deleted.')
        return super().form_valid(form)


# -------------------------------------------------------------------
# API-style views for AJAX calls
# -------------------------------------------------------------------

def product_search_api(request):
    """Quick product search for autocomplete."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(name__icontains=q) | Q(brand__icontains=q),
        status=ProductStatus.ACTIVE
    ).values('id', 'name', 'brand', 'price', 'slug')[:10]

    results = [
        {
            'id': p['id'],
            'name': p['name'],
            'brand': p['brand'],
            'price': str(p['price']),
            'url': f'/products/{p["slug"]}/',
        }
        for p in products
    ]
    return JsonResponse({'results': results})
