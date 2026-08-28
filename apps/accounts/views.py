"""
Views for the accounts application.

Handles user registration, login, logout, profile management,
and role-based redirections.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db import transaction
from django.utils.decorators import method_decorator

from .models import User, UserProfile, LoginHistory
from .forms import (
    UserRegistrationForm, UserLoginForm,
    UserProfileUpdateForm, UserProfileDetailForm,
    CustomPasswordChangeForm
)
from apps.audit.utils import log_action

logger = logging.getLogger('apps.accounts')


def get_client_ip(request: HttpRequest) -> str:
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


class RegisterView(View):
    """Handle user registration for customers and sellers."""

    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display the registration form."""
        if request.user.is_authenticated:
            return redirect(request.user.get_dashboard_url())
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @transaction.atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        """Process the registration form submission."""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile
            UserProfile.objects.get_or_create(user=user)

            # Auto-login after registration
            login(request, user)

            # Log the action
            log_action(
                user=user,
                action='REGISTER',
                module='accounts',
                description=f'New user registered with role: {user.role}'
            )

            messages.success(
                request,
                f'Welcome to ShopAI, {user.get_short_name()}! Your account has been created.'
            )
            logger.info(f'New user registered: {user.email} with role {user.role}')
            return redirect(user.get_dashboard_url())

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    """Custom login view with remember-me and audit logging."""

    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        """Redirect to role-appropriate dashboard."""
        return self.request.user.get_dashboard_url()

    def form_valid(self, form):
        """Handle successful login — record history and audit."""
        user = form.get_user()
        remember_me = form.cleaned_data.get('remember_me', False)

        response = super().form_valid(form)

        # Adjust session expiry
        if not remember_me:
            self.request.session.set_expiry(0)  # Expires when browser closes
        else:
            self.request.session.set_expiry(86400 * 7)  # 7 days

        # Record login history
        LoginHistory.objects.create(
            user=user,
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')[:500],
            was_successful=True,
            session_key=self.request.session.session_key or '',
        )

        # Update user's last login IP
        user.last_login_ip = get_client_ip(self.request)
        user.save(update_fields=['last_login_ip'])

        # Audit log
        log_action(
            user=user,
            action='LOGIN',
            module='accounts',
            description=f'User logged in from IP: {get_client_ip(self.request)}'
        )

        messages.success(
            self.request,
            f'Welcome back, {user.get_short_name()}!'
        )
        logger.info(f'User logged in: {user.email}')
        return response

    def form_invalid(self, form):
        """Handle failed login attempt."""
        email = form.data.get('username', 'unknown')
        logger.warning(f'Failed login attempt for email: {email}')
        return super().form_invalid(form)


class LogoutView(View):
    """Handle user logout."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Log out the user and redirect to home."""
        if request.user.is_authenticated:
            log_action(
                user=request.user,
                action='LOGOUT',
                module='accounts',
                description='User logged out'
            )
            logger.info(f'User logged out: {request.user.email}')

        logout(request)
        messages.info(request, 'You have been successfully logged out.')
        return redirect('/')

    def get(self, request: HttpRequest) -> HttpResponse:
        """Allow GET logout (redirect to login)."""
        return self.post(request)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """View and update user profile."""

    template_name = 'accounts/profile.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display the user profile."""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileUpdateForm(instance=request.user)
        profile_form = UserProfileDetailForm(instance=profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        """Update user profile information."""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user
        )
        profile_form = UserProfileDetailForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            log_action(
                user=request.user,
                action='PROFILE_UPDATE',
                module='accounts',
                description='User updated their profile'
            )

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    """Handle password change requests."""

    template_name = 'accounts/change_password.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            log_action(
                user=request.user,
                action='PASSWORD_CHANGE',
                module='accounts',
                description='User changed their password'
            )

            messages.success(request, 'Your password has been changed successfully.')
            return redirect('accounts:profile')

        return render(request, self.template_name, {'form': form})


def error_404(request, exception=None):
    """Custom 404 error page."""
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    """Custom 500 error page."""
    return render(request, 'errors/500.html', status=500)
