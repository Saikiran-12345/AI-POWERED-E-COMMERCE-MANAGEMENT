"""
Permission decorators and mixins for role-based access control.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden


def customer_required(view_func):
    """Decorator that requires the user to be a CUSTOMER."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not request.user.is_customer:
            messages.error(request, 'Access denied. Customer account required.')
            return redirect(request.user.get_dashboard_url())
        return view_func(request, *args, **kwargs)
    return wrapper


def seller_required(view_func):
    """Decorator that requires the user to be a SELLER."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not request.user.is_seller:
            messages.error(request, 'Access denied. Seller account required.')
            return redirect(request.user.get_dashboard_url())
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator that requires the user to be an ADMIN."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not request.user.is_admin:
            messages.error(request, 'Access denied. Admin account required.')
            return redirect(request.user.get_dashboard_url())
        return view_func(request, *args, **kwargs)
    return wrapper


def seller_or_admin_required(view_func):
    """Decorator that requires the user to be a SELLER or ADMIN."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not (request.user.is_seller or request.user.is_admin):
            messages.error(request, 'Access denied. Seller or Admin account required.')
            return redirect(request.user.get_dashboard_url())
        return view_func(request, *args, **kwargs)
    return wrapper


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for class-based views requiring CUSTOMER role."""

    def test_func(self) -> bool:
        return self.request.user.is_customer

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        messages.error(self.request, 'Access denied. Customer account required.')
        return redirect(self.request.user.get_dashboard_url())


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for class-based views requiring SELLER role."""

    def test_func(self) -> bool:
        return self.request.user.is_seller

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        messages.error(self.request, 'Access denied. Seller account required.')
        return redirect(self.request.user.get_dashboard_url())


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for class-based views requiring ADMIN role."""

    def test_func(self) -> bool:
        return self.request.user.is_admin

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        messages.error(self.request, 'Access denied. Admin account required.')
        return redirect(self.request.user.get_dashboard_url())


class SellerOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for class-based views requiring SELLER or ADMIN role."""

    def test_func(self) -> bool:
        return self.request.user.is_seller or self.request.user.is_admin

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.get_login_url())
        messages.error(self.request, 'Access denied.')
        return redirect(self.request.user.get_dashboard_url())
