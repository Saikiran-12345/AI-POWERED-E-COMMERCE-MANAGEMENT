"""
Product and Category models for the E-Commerce SaaS.

Includes full product management with categories, brands,
pricing, discounts, ratings, and status management.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse
import uuid


class Category(models.Model):
    """
    Product category with optional parent for hierarchy support.
    """

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['sort_order', 'name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('products:category_detail', kwargs={'slug': self.slug})

    @property
    def product_count(self) -> int:
        """Return count of active products in this category."""
        return self.products.filter(status=ProductStatus.ACTIVE).count()

    @property
    def is_top_level(self) -> bool:
        """Check if this is a top-level category."""
        return self.parent is None

    def get_all_products(self):
        """Return all products including from subcategories."""
        products = self.products.filter(status=ProductStatus.ACTIVE)
        for child in self.children.filter(is_active=True):
            products = products | child.get_all_products()
        return products


class ProductStatus(models.TextChoices):
    """Product availability status."""
    ACTIVE = 'ACTIVE', _('Active')
    INACTIVE = 'INACTIVE', _('Inactive')
    OUT_OF_STOCK = 'OUT_OF_STOCK', _('Out of Stock')
    DRAFT = 'DRAFT', _('Draft')
    DISCONTINUED = 'DISCONTINUED', _('Discontinued')


class Product(models.Model):
    """
    Core Product model with all e-commerce fields.

    Supports categories, sellers, pricing, discounts,
    ratings, and full lifecycle management.
    """

    product_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'role': 'SELLER'}
    )
    brand = models.CharField(max_length=200, blank=True, db_index=True)
    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        help_text='Stock Keeping Unit — auto-generated if blank'
    )

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Discount percentage (0-100)'
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Cost price for profit calculation'
    )

    # Media
    main_image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )

    # Status & visibility
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE,
        db_index=True
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_digital = models.BooleanField(
        default=False,
        help_text='Digital products do not require shipping'
    )

    # Ratings (denormalized for performance)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review_count = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated tags'
    )

    # Tracking
    view_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['price', 'average_rating']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        if not self.sku:
            self.sku = f'SKU-{str(self.product_id)[:8].upper()}'
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def discounted_price(self):
        """Calculate the final price after discount."""
        if self.discount_percent > 0:
            discount = self.price * (self.discount_percent / 100)
            return round(self.price - discount, 2)
        return self.price

    @property
    def discount_amount(self):
        """Calculate absolute discount amount."""
        return round(self.price - self.discounted_price, 2)

    @property
    def has_discount(self) -> bool:
        """Check if product has an active discount."""
        return self.discount_percent > 0

    @property
    def stock_quantity(self) -> int:
        """Get current stock quantity from inventory."""
        try:
            return self.inventory.quantity
        except Exception:
            return 0

    @property
    def is_in_stock(self) -> bool:
        """Check if product is currently in stock."""
        return self.stock_quantity > 0 and self.status == ProductStatus.ACTIVE

    @property
    def is_low_stock(self) -> bool:
        """Check if stock is below the low-stock threshold."""
        from django.conf import settings
        threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 10)
        return 0 < self.stock_quantity <= threshold

    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost_price > 0 and self.discounted_price > 0:
            profit = self.discounted_price - self.cost_price
            return round((profit / self.discounted_price) * 100, 2)
        return 0

    def get_tags_list(self) -> list:
        """Return tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

    def increment_view_count(self):
        """Atomically increment the view count."""
        Product.objects.filter(pk=self.pk).update(view_count=models.F('view_count') + 1)

    def update_rating(self):
        """Recalculate average rating from reviews."""
        from django.db.models import Avg, Count
        result = self.reviews.filter(is_approved=True).aggregate(
            avg=Avg('rating'),
            count=Count('id')
        )
        self.average_rating = result['avg'] or 0
        self.review_count = result['count'] or 0
        self.save(update_fields=['average_rating', 'review_count'])


class ProductImage(models.Model):
    """Additional images for a product."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    def __str__(self) -> str:
        return f'Image for {self.product.name}'


class ProductAttribute(models.Model):
    """
    Flexible key-value attributes for products.
    e.g., Color=Red, Size=XL, Material=Cotton
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('product', 'name')
        verbose_name = _('product attribute')
        verbose_name_plural = _('product attributes')

    def __str__(self) -> str:
        return f'{self.product.name}: {self.name} = {self.value}'
