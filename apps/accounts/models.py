"""
Custom User model and related models for the E-Commerce SaaS.

Implements three user roles:
- CUSTOMER: Can shop, review, view recommendations
- SELLER: Can manage products, inventory, view sales
- ADMIN: Full system access
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """Enumeration of user roles in the system."""
    CUSTOMER = 'CUSTOMER', _('Customer')
    SELLER = 'SELLER', _('Seller')
    ADMIN = 'ADMIN', _('Admin')


class UserManager(BaseUserManager):
    """Custom manager for User model with email-based authentication."""

    def create_user(self, email: str, password: str = None, **extra_fields) -> 'User':
        """
        Create and save a regular user with the given email and password.

        Args:
            email: The user's email address (used as username).
            password: The user's password (will be hashed).
            **extra_fields: Additional fields for the User model.

        Returns:
            User: The newly created user instance.

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'User':
        """
        Create and save a superuser (Admin role).

        Args:
            email: The admin's email address.
            password: The admin's password.
            **extra_fields: Additional fields.

        Returns:
            User: The newly created superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRole.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

    def get_customers(self):
        """Return queryset of all customer users."""
        return self.filter(role=UserRole.CUSTOMER, is_active=True)

    def get_sellers(self):
        """Return queryset of all seller users."""
        return self.filter(role=UserRole.SELLER, is_active=True)

    def get_admins(self):
        """Return queryset of all admin users."""
        return self.filter(role=UserRole.ADMIN, is_active=True)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the E-Commerce SaaS platform.

    Uses email as the primary identifier instead of username.
    Supports three roles: CUSTOMER, SELLER, ADMIN.
    """

    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True,
        help_text=_('Required. Enter a valid email address.')
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        db_index=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.')
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    last_login_ip = models.GenericIPAddressField(
        _('last login IP'),
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True
    )
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        null=True,
        blank=True
    )
    is_email_verified = models.BooleanField(
        _('email verified'),
        default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return f'{self.get_full_name()} <{self.email}>'

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name or self.email.split('@')[0]

    @property
    def is_customer(self) -> bool:
        """Check if user has customer role."""
        return self.role == UserRole.CUSTOMER

    @property
    def is_seller(self) -> bool:
        """Check if user has seller role."""
        return self.role == UserRole.SELLER

    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

    def get_dashboard_url(self) -> str:
        """Return the appropriate dashboard URL based on user role."""
        from django.urls import reverse
        role_urls = {
            UserRole.CUSTOMER: 'dashboard:customer',
            UserRole.SELLER: 'dashboard:seller',
            UserRole.ADMIN: 'dashboard:admin',
        }
        return reverse(role_urls.get(self.role, 'dashboard:customer'))


class UserProfile(models.Model):
    """
    Extended profile information for users.

    Stores additional details like address, preferences, bio, etc.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(
        _('bio'),
        blank=True,
        max_length=500
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True
    )
    gender = models.CharField(
        _('gender'),
        max_length=20,
        blank=True,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
            ('P', 'Prefer not to say'),
        ]
    )
    # Address fields
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')

    # Preferences
    newsletter_subscribed = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self) -> str:
        return f'Profile of {self.user.get_full_name()}'

    def get_full_address(self) -> str:
        """Return formatted full address."""
        parts = filter(bool, [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.pincode,
            self.country,
        ])
        return ', '.join(parts)


class LoginHistory(models.Model):
    """
    Records user login history for security monitoring.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_history'
    )
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    was_successful = models.BooleanField(default=True)
    session_key = models.CharField(max_length=40, blank=True)

    class Meta:
        verbose_name = _('login history')
        verbose_name_plural = _('login histories')
        ordering = ['-login_time']

    def __str__(self) -> str:
        return f'{self.user.email} logged in at {self.login_time}'

    @property
    def session_duration(self):
        """Calculate the duration of the login session."""
        if self.logout_time:
            return self.logout_time - self.login_time
        return None
