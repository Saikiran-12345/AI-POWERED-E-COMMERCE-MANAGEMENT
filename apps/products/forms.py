"""
Forms for the products application.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, ProductAttribute


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing products.
    Used by sellers and admins.
    """

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas',
        }),
        help_text=_('Separate tags with commas, e.g.: electronics, mobile, smartphone')
    )

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'short_description', 'category',
            'brand', 'sku', 'price', 'discount_percent', 'cost_price',
            'main_image', 'status', 'is_featured', 'is_digital',
            'meta_title', 'meta_description', 'tags'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed product description',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Short description (max 500 chars)',
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand name',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave blank for auto-generated SKU',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'discount_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'main_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_digital': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (leave blank to use product name)',
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'SEO meta description',
            }),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError(_('Price must be greater than zero.'))
        return price

    def clean_discount_percent(self):
        discount = self.cleaned_data.get('discount_percent', 0)
        if discount < 0 or discount > 100:
            raise forms.ValidationError(_('Discount must be between 0 and 100.'))
        return discount


class CategoryForm(forms.ModelForm):
    """Form for creating and editing product categories."""

    class Meta:
        model = Category
        fields = ('name', 'description', 'image', 'parent', 'is_active', 'sort_order')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class ProductSearchForm(forms.Form):
    """
    Search and filter form for the product listing page.
    """

    q = forms.CharField(
        required=False,
        label=_('Search'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...',
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price',
            'step': '0.01',
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price',
            'step': '0.01',
        })
    )
    min_rating = forms.ChoiceField(
        choices=[('', 'Any Rating'), ('4', '4+'), ('3', '3+'), ('2', '2+')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    in_stock = forms.BooleanField(
        required=False,
        label=_('In Stock Only'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('', 'Default'),
            ('price_asc', 'Price: Low to High'),
            ('price_desc', 'Price: High to Low'),
            ('rating', 'Highest Rated'),
            ('newest', 'Newest First'),
            ('popular', 'Most Popular'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    brand = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brand name',
        })
    )
