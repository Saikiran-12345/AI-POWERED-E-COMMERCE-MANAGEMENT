"""
URL configuration for AI-Powered E-Commerce Management & Recommendation SaaS.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

handler404 = 'apps.accounts.views.error_404'
handler500 = 'apps.accounts.views.error_500'

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Home redirect
    path('', RedirectView.as_view(url='/products/', permanent=False), name='home'),

    # Accounts (auth, profiles)
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),

    # Dashboard (role-based landing)
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # Products & Categories
    path('products/', include('apps.products.urls', namespace='products')),

    # Cart
    path('cart/', include('apps.cart.urls', namespace='cart')),

    # Wishlist
    path('wishlist/', include('apps.wishlist.urls', namespace='wishlist')),

    # Orders
    path('orders/', include('apps.orders.urls', namespace='orders')),

    # Payments
    path('payments/', include('apps.payments.urls', namespace='payments')),

    # Customers
    path('customers/', include('apps.customers.urls', namespace='customers')),

    # Sellers
    path('sellers/', include('apps.sellers.urls', namespace='sellers')),

    # Inventory
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),

    # Reviews
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),

    # Recommendations
    path('recommendations/', include('apps.recommendations.urls', namespace='recommendations')),

    # Analytics
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),

    # Reports
    path('reports/', include('apps.reports.urls', namespace='reports')),

    # Notifications
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),

    # Audit Logs
    path('audit/', include('apps.audit.urls', namespace='audit')),

    # ML
    path('ml/', include('apps.ml.urls', namespace='ml')),

    # Forecasting
    path('forecasting/', include('apps.forecasting.urls', namespace='forecasting')),

    # Fraud Detection
    path('fraud/', include('apps.fraud_detection.urls', namespace='fraud_detection')),

    # REST API v1
    path('api/v1/', include([
        path('auth/', include('apps.accounts.api_urls', namespace='api_auth')),
        path('products/', include('apps.products.api_urls', namespace='api_products')),
        path('cart/', include('apps.cart.api_urls', namespace='api_cart')),
        path('wishlist/', include('apps.wishlist.api_urls', namespace='api_wishlist')),
        path('orders/', include('apps.orders.api_urls', namespace='api_orders')),
        path('reviews/', include('apps.reviews.api_urls', namespace='api_reviews')),
        path('recommendations/', include('apps.recommendations.api_urls', namespace='api_recommendations')),
        path('analytics/', include('apps.analytics.api_urls', namespace='api_analytics')),
        path('notifications/', include('apps.notifications.api_urls', namespace='api_notifications')),
        path('inventory/', include('apps.inventory.api_urls', namespace='api_inventory')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
