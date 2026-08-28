"""
URL patterns for the products application.
"""

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Public
    path('', views.ProductListView.as_view(), name='list'),
    path('search/', views.product_search_api, name='search_api'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),

    # Seller/Admin product management
    path('manage/', views.SellerProductListView.as_view(), name='seller_list'),
    path('manage/add/', views.ProductCreateView.as_view(), name='create'),
    path('manage/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='update'),
    path('manage/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete'),

    # Admin category management
    path('admin/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('admin/categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('admin/categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('admin/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
